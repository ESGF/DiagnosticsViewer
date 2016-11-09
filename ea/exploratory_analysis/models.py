from django.db import models
from django.conf import settings
from django.utils.text import slugify
import os
import hashlib
import json
from output_viewer.page import Page
import collections
import package_cache

# Create your models here.


class UserGroup(models.Model):
    """
    Used to make datasets available to other users
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="owned_groups")
    name = models.TextField()
    datasets = models.ManyToManyField("Dataset", related_name="groups", blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="group_memberships", blank=True)
    view_key = models.TextField(blank=True)  # Provide unauthenticated access to this group's content

    def save(self):
        if not self.view_key:
            random_bytes = os.urandom(32)
            self.view_key = ''.join(x.encode('hex') for x in random_bytes)
        super(UserGroup, self).save()


class UserKey(models.Model):
    """
    Used to sign API calls for a user.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    key = models.CharField(max_length=128, unique=True)


class Dataset(models.Model):
    """
    Keeps track of relevant information about a dataset
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.TextField()
    should_rebuild = models.DateTimeField(blank=True)

    @property
    def path(self):
        hasher = hashlib.sha256()
        hasher.update(str(self.owner.id))
        hasher.update(self.name)
        return os.path.join(settings.CONFIG.get("paths", "dataPath"), hasher.hexdigest())

    @property
    def proper_name(self):
        if os.path.exists(self.path):
            for f in os.listdir(self.path):
                if f.endswith("index.json"):
                    with open(os.path.join(self.path, f)) as index:
                        spec = json.load(index)
                    return spec["version"]
        return ""

    @property
    def packages(self):
        indices = []
        for f in os.listdir(self.path):
            if f.endswith("index.json") and f[-11] == "-":
                indices.append(f[:-11])
        return indices

    def query_package(self, package, page=None, group=None, row=None, col=None):
        ind = self.package_index(package)
        pages = []
        for i, p in enumerate(ind["specification"]):
            if page is not None:
                if i == page or p["title"] == page:
                    break
            else:
                pages.append(p["title"])
        else:
            if page is None:
                return pages
            else:
                raise ValueError("No page %s in package %s of DataSet %d" % (page, package, self.id))

        groups = []
        for i, g in enumerate(p["groups"]):
            if group is not None:
                if i == group or g["title"] == group:
                    break
            else:
                groups.append(g["title"])
        else:
            if group is None:
                return groups
            else:
                raise ValueError("No group %s in page %s of package %s of DataSet %d" % (group, page, package, self.id))

        row_index = i
        rows = []
        for i, r in enumerate(p["rows"][row_index]):
            if row is not None:
                if i == row or r["title"] == row:
                    break
            else:
                rows.append(r["title"])
        else:
            if row is None:
                return rows
            else:
                raise ValueError("No row %s in group %s in page %s of package %s of DataSet %d" % (row, group, page, package, self.id))

        cols = []
        if col is None and "columns" in g:
            return g["columns"]

        for i, c in enumerate(r["columns"]):
            col_name = c["title"] if isinstance(c, dict) else g.get("columns", c)
            if col is not None:
                if i == col or col_name == col:
                    break
            else:
                cols.append(col_name)
        else:
            if col is None:
                return cols
            else:
                raise ValueError("No col %s in row %s of group %s in page %s of package %s of DataSet %d" % (col, row, group, page, package, self.id))

        if isinstance(c, dict):
            if "files" in c:
                to_del = []
                l = list(c["files"])
                for i, f in enumerate(c["files"]):
                    path = self.file_path(package, f["url"])
                    if not os.path.exists(path):
                        to_del.append(i)
                for ind in to_del:
                    del l[ind]
                c["files"] = l
        return c

    def index(self):
        """
        Returns the entire tree of packages down to the keys of the columns.
        """
        packages = collections.OrderedDict()
        for pkg in self.packages:
            packages[pkg] = collections.OrderedDict()
            for page in self.query_package(pkg):
                packages[pkg][page] = collections.OrderedDict()
                for grp in self.query_package(pkg, page):
                    packages[pkg][page][grp] = collections.OrderedDict()
                    for row in self.query_package(pkg, page, grp):
                        packages[pkg][page][grp][row] = self.query_package(pkg, page, grp, row)
        return packages

    def union(self, package=None, page=None, group=None, row=None, col=None, *datasets):
        union_index = self.index()
        for ds in datasets:
            new_index = ds.index()
            for package in new_index:
                if package not in union_index:
                    union_index[package] = new_index[package]
                else:
                    for page in package:
                        if page not in union_index[package]:
                            union_index[package][page] = new_index[package][page]
                        else:
                            for grp in page:
                                if grp not in union_index[package][page]:
                                    union_index[package][page][grp] = new_index[package][page][grp]
                                else:
                                    for row in grp:
                                        if row not in union_index[package][page][grp]:
                                            union_index[package][page][grp][row] = new_index[package][page][grp][row]
                                        else:
                                            for col in new_index[package][page][grp][row]:
                                                if col not in union_index[package][page][grp][row]:
                                                    union_index[package][page][grp][row].append(col)
        return union_index

    def package_index(self, pkg):
        if self.package_exists(pkg):
            return package_cache.get_index(self, pkg)
        else:
            return None

    def package_exists(self, pkg):
        return pkg in self.packages

    def file_path(self, pkg, path):
        path, ext = os.path.splitext(path)
        path = slugify(path)
        path = path + ext

        if path.startswith("%s-" % pkg):
            file_path = os.path.join(self.path, path)
        else:
            file_path = os.path.join(self.path, "%s-%s" % (pkg, path))

        return file_path

    def is_package_built(self, pkg):
        index = self.package_index(pkg)
        for spec in index["specification"]:
            if "short_name" not in spec:
                spec["short_name"] = spec["title"].split()[0].lower()
            spec_path = os.path.join(self.path, "%s-%s" % (pkg, spec["short_name"]))
            if not os.path.exists(spec_path):
                return False
        return True

    def user_has_access(self, user, groups=None):
        if user.is_authenticated() and user.id == self.owner.id:
            return True
        found = False
        if groups is not None:
            try:
                group = self.groups.filter(id__in=[g.id for g in groups])
                return True
            except UserGroup.DoesNotExist:
                return False
        return False

    def rebuild(self):
        # Should now rebuild the pages in case of updates
        for package in self.packages:
            index = self.package_index(package)
            for spec in index["specification"]:
                if "short_name" not in spec:
                    spec["short_name"] = spec["title"].split()[0].lower()
                # Hack the filename to have the package prefix
                for group in spec["rows"]:
                    for row in group:
                        for col in row["columns"]:
                            if isinstance(col, dict):
                                if "path" in col:
                                    p = col["path"]
                                    fname, ext = os.path.splitext(p)
                                    fname = os.path.join(package, fname)
                                    fname = "--".join(fname.split(os.sep))
                                    fpath = slugify(fname) + ext
                                    col["path"] = fpath

                p = Page(spec, root_path=self.path)
                p.build(os.path.join(self.path, "%s-%s" % (package, spec["short_name"])))
