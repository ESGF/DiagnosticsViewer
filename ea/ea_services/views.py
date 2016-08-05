from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
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
import datetime
import hmac
from django.conf import settings
import hashlib
from django.forms.models import model_to_dict
from django.utils import timezone
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
        print "no userid"
        return False
    if "HTTP_X_SIGNATURE" not in request.META:
        print "no signature"
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
        print "User doesn't exist"
        return False
    except UserKey.DoesNotExist:
        print "Key doesn't exist"
        return False
    except ValueError as e:
        print "Bad signature"
        return False


def share_dataset(request):
    if request.method != "POST":
        h = HttpResponse(status="405")
        h["Allow"] = "POST"
        return h

    user = auth_and_validate(request)
    if user is False:
        return JsonResponse({"error": "Invalid credentials."}, status="403")

    gid = request.POST.get("group", None)
    if gid is None:
        return JsonResponse({"error": "No group provided."}, status="400")

    try:
        g = user.group_memberships.get(id=gid)
    except UserGroup.DoesNotExist:
        try:
            g = user.owned_groups.get(id=gid)
        except UserGroup.DoesNotExist:
            return JsonResponse({"error": "User not in any group matching request."}, status="400")

    ds_id = request.POST.get('dataset', None)
    if ds_id is None:
        return JsonResponse({"error": "No dataset provided."}, status="400")

    try:
        ds = user.dataset_set.get(id=ds_id)
    except Dataset.DoesNotExist:
        return JsonResponse({"error": "User does not own any dataset matching request."}, status="400")

    try:
        in_group = g.datasets.get(id=ds_id)
    except Dataset.DoesNotExist:
        pass
    else:
        return JsonResponse({"error": "Dataset already shared with group."}, status="400")

    g.datasets.add(ds)
    g.save()
    return JsonResponse({"status": "success"})


def remove_user_from_group(request, gid):
    if request.method != "POST":
        h = HttpResponse(status="405")
        h["Allow"] = "POST"
        return h

    user = auth_and_validate(request)
    if user is False:
        return JsonResponse({"error": "Invalid credentials."}, status="403")

    uid = request.POST.get("user", None)
    if uid is None:
        return JsonResponse({"error": "No user provided."}, status="400")
    uid = int(uid)

    try:
        g = UserGroup.objects.get(id=gid)
    except UserGroup.DoesNotExist:
        return JsonResponse({"error": "No such group."}, status="400")

    if g.owner.id != user.id and user.id != uid:
        return JsonResponse({"error": "You don't own this group."}, status="403")

    try:
        u = User.objects.get(id=uid)
    except User.DoesNotExist:
        return JsonResponse({"error": "No such user."}, status="400")

    try:
        g.members.get(id=uid)
    except User.DoesNotExist:
        in_group = False
    else:
        in_group = True

    if in_group is False:
        return JsonResponse({"error": "User not found in group."}, status="400")

    g.members.remove(u)
    g.save()

    return JsonResponse({"status": "success"})


def add_user_to_group(request, gid):
    if request.method != "POST":
        h = HttpResponse(status="405")
        h["Allow"] = "POST"
        return h

    user = auth_and_validate(request)
    if user is False:
        return JsonResponse({"error": "Invalid credentials."}, status="403")

    uid = request.POST.get("user", None)
    if uid is None:
        return JsonResponse({"error": "No user provided."}, status="400")

    try:
        g = UserGroup.objects.get(id=gid)
    except UserGroup.DoesNotExist:
        return JsonResponse({"error": "No such group."}, status="400")

    if g.owner.id != user.id:
        return JsonResponse({"error": "You don't own this group."}, status="403")

    try:
        u = User.objects.get(id=uid)
    except User.DoesNotExist:
        return JsonResponse({"error": "No such user."}, status="400")

    try:
        g.members.get(id=uid)
    except User.DoesNotExist:
        in_group = False
    else:
        in_group = True

    if user.id == int(uid) or in_group is True:
        return JsonResponse({"error": "User already in group."}, status="400")

    g.members.add(u)
    g.save()

    return JsonResponse({"status": "success"})


def search_users(request):
    user = auth_and_validate(request)
    if user is False:
        return HttpResponse("Invalid credentials.", status="403")

    term = request.GET.get("term", None)
    if term is None:
        return HttpResponse("No search term provided.", status="400")

    words = term.split()

    users = User.objects.all()
    user_scores = []

    for u in users:
        u_strings = [u.username, u.email, u.last_name, u.first_name]
        # Compute string similarity
        scores = []
        for s in u_strings:
            if not s:
                scores.append([len(word) * 10 for word in words])
                continue
            word_scores = []
            for word in words:
                substring_scores = []
                for substring in [s[i:i+len(word)] for i in range(max(len(s) - len(word), 1))]:
                    score = 0
                    for i, c in enumerate(substring):
                        if c != word[i]:
                            score += 10
                    substring_scores.append(score)
                score = min(substring_scores)
                word_scores.append(score)
            scores.append(word_scores)

        not_matching = 0
        for score in scores:
            for i, s in enumerate(score):
                print i, s, len(words[i]) * 10
                if s == len(words[i]) * 10:
                    not_matching += 1
        if not_matching == len(scores) * len(words):
            continue
        user_scores.append((scores, u))

    # Sort the users
    sorted_users = sorted(user_scores, key=lambda x: x[0])
    vals = {}
    users = []
    for u in sorted_users:
        user = u[1]
        users.append({
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "email": user.email,
            "id": user.id,
            "scores": {
                "username": u[0][0],
                "email": u[0][1],
                "last_name": u[0][2],
                "first_name": u[0][3]
            }
        })
    vals["users"] = users
    return JsonResponse(vals)


class CredentialsView(View):
    def post(self, request, username):
        password = request.POST.get("password", None)
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


@csrf_exempt
def upload_files(request, dataset_name):
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
    finally:
        # Set it to rebuild in a long time (1 day is enough, since the uploader limits upload sizes.)
        dataset.should_rebuild = timezone.now() + datetime.timedelta(1)
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

    # 5 minutes should be enough for any further uploads to get started; once that
    # time is done, the cron job will take care of the rest.
    dataset.should_rebuild = timezone.now() + datetime.timedelta(0, 300)
    dataset.save()
    return HttpResponse("Success")
