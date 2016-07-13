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
    datasets = models.ManyToManyField("Dataset", blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="group_memberships", blank=True)


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
