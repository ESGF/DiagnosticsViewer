from django.db import models
from django.conf import settings
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

    def user_has_access(self, user, groups=None):
        if user.is_authenticated() and user.id == self.owner.id:
            return True
        found = False
        if groups is not None:
            try:
                group = self.groups.objects.filter(id__in=[g.id for g in groups])
                return True
            except UserGroup.DoesNotExist:
                return False
        return False
