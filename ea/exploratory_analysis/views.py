from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.core.urlresolvers import reverse
import pkg_resources
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
from urllib import urlencode
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

        shared_groups = []
        shared_groups = request.session.get("groups", [])
        if len(shared_groups) == 0 and not request.user.is_authenticated():
            return redirect('login-page')

        groups = list(UserGroup.objects.filter(id__in=shared_groups))

        if request.user.is_authenticated():
            groups.extend(request.user.group_memberships.all())
            groups.extend(request.user.owned_groups.all())

        kwargs["groups"] = groups
        return f(request, *args, **kwargs)
    return wrap


def register(request):

    if request.user.is_authenticated():
        redirect("browse-datasets")

    if request.method == "GET":
        if settings.RECAPTCHA_ENABLED:
            from captcha.client import displayhtml
            errcode = request.GET.get("captcha_error", None)
            captcha_widget = displayhtml(settings.RECAPTCHA_PUBLIC_KEY, {}, error=errcode, use_ssl=True)
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
            challenge = request.POST.get("recaptcha_challenge_field", None)
            if None in (response, challenge):
                messages.error(request, "Please fill out the captcha, and make sure javascript is enabled.")
                return redirect("register-account")

            # Get the IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            resp = submit(challenge, response, settings.RECAPTCHA_PRIVATE_KEY, ip, use_ssl=True)
            if not resp.is_valid:
                messages.error(request, "Please fill out the captcha correctly.")
                return HttpResponseRedirect(reverse("register-account") + "?captcha_error=" + resp.error_code)

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

        if dataset.package_exists(package):
            if dataset.is_package_built(package):
                template = loader.get_template("exploratory_analysis/output_index.html")
                return HttpResponse(template.render({"spec": dataset.package_index(package), "package": package}))
            else:
                dataset.rebuild()
                return HttpResponse("Please wait while package %s is built for viewing..." % package)
        else:
            return HttpResponse("Package %s hasn't been uploaded to this dataset." % package, status="404")
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
            try:
                f = pkg_resources.resource_stream("output_viewer", os.path.join("static", "css", filename))
            except Exception as e:
                print e
                return HttpResponse(status="404")
        elif filename.endswith('js'):
            mime = "text/javascript"
            try:
                f = pkg_resources.resource_stream("output_viewer", os.path.join("static", "js", filename))
            except Exception as e:
                print e
                return HttpResponse(status="404")
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
        datasets = list(request.user.dataset_set.all())
    else:
        datasets = []
    for group in groups:
        datasets.extend(group.datasets.all())

    if "dataset" in request.GET:
        requested = [int(i) for i in request.GET["dataset"].split(",")]
        selected = []
        for ds in datasets:
            if ds.id in requested:
                selected.append(ds)
    else:
        if len(datasets) > 0:
            selected = [datasets[0]]
        else:
            selected = []

    template = loader.get_template("exploratory_analysis/browse.html")
    rc = RequestContext(request, {"datasets": datasets, "selected": selected})
    return HttpResponse(template.render(rc))


def get_selector(request):
    pkg = request.GET.get("package", None)
    page = request.GET.get("page", None)
    group = request.GET.get("group", None)
    row = request.GET.get("row", None)
    col = request.GET.get("col", None)
    return [pkg, page, group, row, col]


@shared_or_login
def compare_datasets(request, groups=None):
    if request.user.is_authenticated():
        source_datasets = list(request.user.dataset_set.all())
    else:
        source_datasets = []
    for group in groups:
        source_datasets.extend(group.datasets.all())

    requested_datasets = request.GET.get("datasets", None)
    if requested_datasets is None:
        raise ValueError("Please specify at least one dataset.")

    requested_datasets = [int(i) for i in requested_datasets.split(",")]
    if len(requested_datasets) < 1:
        raise ValueError("Please specify at least one dataset.")
    real_datasets = []
    for rd in requested_datasets:
        for sd in source_datasets:
            if rd == sd.id:
                real_datasets.append(sd)
                break
        else:
            raise ValueError("No dataset matching %d found." % (rd))

    sel = get_selector(request)

    union_index = real_datasets[0].union(real_datasets[1:])
    index_groups = []
    ind_iter = union_index
    parent_iter = None
    names = "package", "page", "group", "row", "col"

    # Build the navigation
    for ind, i in enumerate(sel[:-1]):
        if i is None:
            break
        s = sel[:ind]
        n = names[:ind]
        d = dict(zip(n, s))
        d["datasets"] = ",".join([str(ds_id) for ds_id in requested_datasets])
        group_rows = []
        for r in ind_iter:
            d[names[ind]] = r
            group_rows.append({"url": reverse("compare") + "?" + urlencode(d), "title": r})
        index_groups.append({"title": i, "rows": group_rows})
        parent_iter = ind_iter
        ind_iter = ind_iter[i]

    template = loader.get_template("exploratory_analysis/viewer.html")
    values = {
        "index_groups": index_groups,
        "datasets": real_datasets,
        "ds_ids": requested_datasets
    }

    # Build the content
    for n, s in zip(names, sel):
        if s is None:
            break
        values[n] = s
    else:
        values["cols"] = ind_iter
        col = []
        for ds in real_datasets:
            try:
                col.append(ds.query_package(*sel)["path"])
            except ValueError:
                col.append(None)
        values["col"] = col

    if "cols" not in values:
        if n != "col":
            values[n + "s"] = ind_iter.keys()
        else:
            values[n + "s"] = ind_iter

    rc = RequestContext(request, values)
    return HttpResponse(template.render(rc))
