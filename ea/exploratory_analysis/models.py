from django.db import models
from django.conf import settings
from django.utils.text import slugify
import os
import hashlib
import json


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

    def package_index(self, pkg):
        if self.package_exists(pkg):
            with open(os.path.join(self.path, "%s-index.json" % pkg)) as ind:
                return json.load(ind)
        else:
            return None

    def package_exists(self, pkg):
        return pkg in self.packages

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
