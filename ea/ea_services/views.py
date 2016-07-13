from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from exploratory_analysis.models import UserKey
from django.utils.crypto import constant_time_compare
from django.utils.text import slugify
import json
import logging
import traceback
import os
import binascii
import urllib
import hmac
from django.conf import settings
import hashlib
from exploratory_analysis.models import *

config = settings.CONFIG
logger = logging.getLogger('exploratory_analysis')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('exploratory_analysis.log')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object
logger.addHandler(fh)

# Create your views here.


def index(request):
    return HttpResponse("ea services index")


def auth_and_validate(request):
    if request.user.is_authenticated():
        return request.user
    body = request.body
    if "HTTP_X_USERID" not in request.META:
        return False
    if "HTTP_X_SIGNATURE" not in request.META:
        return False
    try:
        u = User.objects.get(id__exact=int(request.META["HTTP_X_USERID"]))
        key = u.userkey
        h = hmac.new(key.key, body, hashlib.sha256)
        digested = h.hexdigest()
        if not hmac.compare_digest(digested, request.META["HTTP_X_SIGNATURE"]):
            raise ValueError("Invalid signature.")
        return u
    except User.DoesNotExist:
        return False
    except UserKey.DoesNotExist:
        return False
    except ValueError as e:
        return False


class CredentialsView(View):
    def get(self, request, username):
        password = request.GET.get("password", None)
        if password is None:
            raise ValueError("No password.")
        user = authenticate(username=username, password=password)
        if user.is_active:
            try:
                key = user.userkey
            except UserKey.DoesNotExist:
                pk = binascii.hexlify(os.urandom(128))[:128]
                key = UserKey(user=user, key=pk)
                key.save()
            return JsonResponse({"key": key.key, "id": user.id})


class UploadView(View):
    def post(self, request, dataset_name):
        user = auth_and_validate(request)
        if user is False:
            return HttpResponse("Invalid credentials.", status="403")

        whitelist = ["nc", "hdf5", "hdf4", "bin", "ascii", "text", "txt",
                     "grib", "grb", "ctl", "xml", "pp", "dic", "jpg", "jpeg",
                     "webp", "gif", "png", "apng", "tiff", "bmp", "ico", "svg",
                     "pdf"]
        try:
            dataset = Dataset.objects.get(name=dataset_name, owner=user)
        except Dataset.DoesNotExist:
            dataset = Dataset(name=dataset_name, owner=user)
            dataset.save()

        path = dataset.path
        if not os.path.exists(path):
            os.makedirs(path)

        for f in request.FILES:
            fname, ext = os.path.splitext(f)
            fname = "--".join(fname.split(os.sep))
            fpath = os.path.join(path, slugify(fname) + ext)
            with open(fpath, "wb+") as upload:
                for chunk in request.FILES[f].chunks():
                    upload.write(chunk)
        return HttpResponse("Success")
