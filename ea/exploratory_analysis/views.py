from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.template import RequestContext, loader
import json
from django.contrib.auth import authenticate, login
from django.conf import settings
from metrics.frontend import lmwgmaster
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.templatetags.static import static
#from metrics.frontend.lmwgmaster import *
from django.contrib.staticfiles.storage import staticfiles_storage

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Dataset, UserGroup

import json
import logging
import traceback
import os
import shutil
from output_viewer.page import Page

from utils import isLoggedIn, generate_token_url

logger = logging.getLogger('exploratory_analysis')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('exploratory_analysis.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object
logger.addHandler(fh)

config = settings.CONFIG


def index(request):

    template = loader.get_template('exploratory_analysis/index.html')
    user = request.user
    if request.user.is_authenticated():
        username = user.username
    else:
        username = ''

    context = RequestContext(request, {
        'username': username,
    })

    return HttpResponse(template.render(context))


def login_page(request):

    template = loader.get_template('exploratory_analysis/login.html')

    context = RequestContext(request, {})

    return HttpResponse(template.render(context))


@login_required
def logout_page(request):
    from django.contrib.auth import logout
    logout(request)

    template = loader.get_template('exploratory_analysis/logout.html')

    loggedIn = False

    context = RequestContext(request, {
        'loggedIn' : str(loggedIn)
    })

    return HttpResponse(template.render(context))


@login_required
def output(request, dataset, package):
    try:
        dataset = Dataset.objects.get(name=dataset, owner=request.user)
        package_index = os.path.join(dataset.path, "%s-index.json" % package)
        if os.path.exists(package_index):
            # Should now rebuild the pages in case of updates
            with open(package_index) as ind:
                index = json.load(ind)
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

                p = Page(spec, root_path=dataset.path)
                p.build(os.path.join(dataset.path, "%s-%s" % (package, spec["short_name"])))
            template = loader.get_template("exploratory_analysis/output_index.html")
            return HttpResponse(template.render({"spec": index, "package": package}))
        else:
            return HttpResponse("No package matching %s found." % package, status="404")
    except Dataset.DoesNotExist:
        return HttpResponse("No dataset matching %s found for user." % dataset, status="404")


@login_required
def view_group_memberships(request):
    rc = RequestContext(request, {})
    template = loader.get_template("exploratory_analysis/groups.html")
    return HttpResponse(template.render(rc))


@login_required
def invite_to_group(request, group_id):
    return HttpResponse("thumbs up")


@login_required
def leave_group(request, group_id):
    return HttpResponse("thumbs up")


@login_required
def create_group(request):
    if request.method != "POST":
        r = HttpResponse()
        r.status_code = 405
        return r
    expects = request.META.get("HTTP_EXPECT", "text/html")

    r = HttpResponse()
    if expects.lower() == "application/json":
        # it's an ajax call
        data = json.loads(request.body)
        r.content_type = "application/json"
    else:
        # it's a page request
        data = request.POST

    if "name" not in data:
        r.status_code = 400
        reason = "name attribute not provided."

    try:
        group = UserGroup.objects.get(name=data["name"])
    except UserGroup.DoesNotExist:
        group = UserGroup(name=data["name"], owner=request.user)
        group.save()
    else:
        r.status_code = 400
        reason = "Group already exists"

    if r.status_code != 200:
        if expects.lower() == "application/json":
            r.body = json.dumps({"reason": reason})
        else:
            r.body = reason
    else:
        if expects.lower() == "application/json":
            r.body = json.dumps({"id": group.id, "name": group.name})
        else:
            return redirect(view_group_memberships)

    return r


@login_required
def output_file(request, dataset, package, path):
    try:
        dataset = Dataset.objects.get(name=dataset, owner=request.user)
    except Dataset.DoesNotExist:
        # Need to check if user is in group with access to dataset
        return HttpResponse("No dataset matching %s found for user." % dataset, status="404")

    package_index = os.path.join(dataset.path, "%s-index.json" % package)
    if not os.path.exists(package_index):
        return HttpResponse("No package %s found." % package, status="404")

    if path.startswith("viewer"):
        # Map to our scripts/css files
        _, filename = os.path.split(path)
        if filename.endswith("css"):
            mime = "text/css"
            if filename.startswith("bootstrap"):
                f = open(staticfiles_storage.path("exploratory_analysis/css/bootstrap/bootstrap.css"))
            elif filename.startswith("viewer"):
                f = open(staticfiles_storage.path("exploratory_analysis/css/viewer.css"))
        elif filename.endswith('js'):
            mime = "text/javascript"
            if filename.lower().startswith("jquery"):
                f = open(staticfiles_storage.path('exploratory_analysis/js/jquery/jquery-1.10.2.min.js'))
            elif filename.lower().startswith("viewer"):
                f = open(staticfiles_storage.path('exploratory_analysis/js/viewer.js'))
            elif filename.lower().startswith("bootstrap"):
                f = open(staticfiles_storage.path('exploratory_analysis/js/bootstrap/bootstrap.min.js'))
        return HttpResponse(f, content_type=mime)

    if path.startswith("%s-" % package):
        file_path = os.path.join(dataset.path, path)
    else:
        file_path = os.path.join(dataset.path, "%s-%s" % (package, path))

    if not os.path.exists(file_path):
        return HttpResponse("No file %s found in package." % file_path, status="404")

    return HttpResponse(open(file_path))


@login_required
def browse_datasets(request):
    datasets = request.user.dataset_set.all()
    template = loader.get_template("exploratory_analysis/browse.html")
    rc = RequestContext(request, {"datasets": datasets})
    return HttpResponse(template.render(rc))


def auth(request):
    if request.user.is_authenticated():
        redirect("index")

    if request.method == "POST":
        user = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=user, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('index')

    return redirect("login")
