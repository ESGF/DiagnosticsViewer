from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
import json
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.templatetags.static import static
from django.contrib import messages
from django.contrib.staticfiles.storage import staticfiles_storage

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Dataset, UserGroup
from django.contrib.auth.models import User

import json
import logging
import traceback
import os
import shutil
from output_viewer.page import Page


logger = logging.getLogger('exploratory_analysis')
logger.setLevel(logging.WARNING)

fh = logging.FileHandler('exploratory_analysis.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object
logger.addHandler(fh)

config = settings.CONFIG


def shared_or_login(f):
    """
    Allows anonymous "logins" of shared group content.

    Functions using this decorator must accept a "groups" keyword argument.
    """
    def wrap(request, *args, **kwargs):
        groups = None

        if request.user.is_authenticated():
            groups = request.user.group_memberships.all()
        else:
            groups = request.session.get("groups", [])
            if len(groups) == 0:
                return redirect('login-page')
            groups = UserGroup.objects.filter(id__in=groups)

        kwargs["groups"] = groups
        return f(request, *args, **kwargs)
    return wrap


def register(request):

    if request.user.is_authenticated():
        redirect("browse-datasets")

    if request.method == "GET":
        if settings.RECAPTCHA_ENABLED:
            from captcha.client import displayhtml
            captcha_widget = displayhtml(settings.RECAPTCHA_PUBLIC_KEY, {}, use_ssl=True)
        else:
            captcha_widget = None

        vals = {
            "captcha": captcha_widget,
        }

        ctx = RequestContext(request, vals)
        template = loader.get_template("exploratory_analysis/register_user.html")
        return HttpResponse(template.render(ctx))
    elif request.method == "POST":

        if settings.RECAPTCHA_ENABLED:
            # Validate the captcha
            from captcha.client import submit
            response = request.POST.get('recaptcha_response_field', None)
            challenge = request.POST.get("recaptca_challenge_field", None)
            if None in (response, challenge):
                messages.error(request, "Please fill out the captcha correctly.")
                return redirect("register-account")

            # Get the IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            resp = submit(response, challenge, settings.RECAPTCHA_PRIVATE_KEY, ip, use_ssl=True)
            if not resp.is_valid:
                messages.error(request, "Please fill out the captcha correctly.")
                return redirect("register-account")

        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        email = request.POST.get("email", None)

        if None in (username, password, email):
            messages.error(request, "Username, password, and email are required fields.")
            return redirect("register-account")

        first_name = request.POST.get("first_name", None)
        last_name = request.POST.get("last_name", None)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User(username=username, email=email, first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.is_active = True
            user.save()
        else:
            messages.error(request, "Username taken.")
            return redirect("register-account")

        u = authenticate(username=username, password=password)

        if u is not None:
            if u.is_active is False:
                messages.error(request, "There's been an error registering your account. Please contact support with your desired username.")
                return redirect("register-account")
            messages.success(request, "Welcome to the site!")
            login(request, u)
            return redirect("browse-datasets")
        else:
            messages.error(request, "Unable to register user.")
            return redirect("register-account")


def auth(request):
    if request.user.is_authenticated():
        redirect("browse-datasets")

    if request.method == "POST":
        user = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=user, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('browse-datasets')

    return redirect("login-page")


def login_page(request):
    template = loader.get_template('exploratory_analysis/login.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))


def anonymous_login(request, share_key):
    try:
        group = UserGroup.objects.get(view_key=share_key)
    except UserGroup.DoesNotExist:
        messages.error(request, "Invalid shared URL.")
        return redirect("login-page")

    groups = request.session.get("groups", [])
    if group.id not in groups:
        groups.append(group.id)
    request.session["groups"] = groups
    return redirect('browse-datasets')


@login_required
def logout_page(request):
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'Logged Out')

    return redirect("login-page")


@shared_or_login
def output(request, dataset, package, groups=None):
    try:
        dataset = Dataset.objects.get(id=dataset)

        if not dataset.user_has_access(request.user, groups):
            raise Dataset.DoesNotExist()

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
def manage_group(request, group_id):
    try:
        error = None
        group = UserGroup.objects.get(id=group_id)
        if request.user.id != group.owner.id:
            error = "You don't own that group."
    except UserGroup.DoesNotExist:
        error = "No group found."

    if error is not None:
        messages.error(request, error)
        return redirect("view-groups")

    vals = {"group": group, "share": request.build_absolute_uri(reverse("anonymous-login", args=[group.view_key]))}
    rc = RequestContext(request, vals)
    template = loader.get_template("exploratory_analysis/group_page.html")
    return HttpResponse(template.render(rc))


@login_required
def create_group(request):
    if request.method != "POST":
        r = HttpResponse()
        r.status_code = 405
        return r
    expects = request.META.get("HTTP_EXPECT", "text/html")

    r = HttpResponse(status=200)
    if expects.lower() == "application/json":
        # it's an ajax call
        data = json.loads(request.body)
        r.content_type = "application/json"
    else:
        # it's a page request
        data = request.POST

    if "name" not in data:
        r.status_code = 400
        reason = "No name provided for group."

    try:
        group = UserGroup.objects.get(name=data["name"])
    except UserGroup.DoesNotExist:
        group = UserGroup(name=data["name"], owner=request.user)
        group.save()
    else:
        r.status_code = 400
        reason = "Group '%s' already exists." % data["name"]

    if r.status_code != 200:
        if expects.lower() == "application/json":
            r.body = json.dumps({"reason": reason})
        else:
            messages.error(request, reason)
            return redirect(view_group_memberships)
    else:
        if expects.lower() == "application/json":
            r.body = json.dumps({"id": group.id, "name": group.name})
        else:
            return redirect(view_group_memberships)

    return r


@shared_or_login
def output_file(request, dataset, package, path, groups=None):
    try:
        dataset = Dataset.objects.get(id=dataset)
    except Dataset.DoesNotExist:
        # Need to check if user is in group with access to dataset
        return HttpResponse("No dataset matching %s found." % dataset, status="404")

    if request.user.is_authenticated():
        user_id = request.user.id
    else:
        user_id = None

    if dataset.owner.id != user_id:
        found = False
        for group in groups:
            try:
                group.datasets.get(id=dataset.id)
            except Dataset.DoesNotExist:
                pass
            else:
                found = True
        if found is False:
            return HttpResponse("User does not have access to dataset %s" % dataset, status="404")

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


@shared_or_login
def browse_datasets(request, groups=None):
    if request.user.is_authenticated():
        datasets = request.user.dataset_set.all()
    else:
        datasets = []
    for group in groups:
        datasets.extend(group.datasets.all())
    print groups, datasets
    template = loader.get_template("exploratory_analysis/browse.html")
    for ds in datasets:
        print ds.packages
    rc = RequestContext(request, {"datasets": datasets})
    return HttpResponse(template.render(rc))
