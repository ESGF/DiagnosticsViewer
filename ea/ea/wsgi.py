"""
WSGI config for ea project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys
import site

app_root = os.path.dirname(os.path.dirname(__file__))

# Requires environment to be installed above the app_root and named "env"
site.addsitedir(os.path.join(os.path.dirname(app_root), "env", "lib", "python2.7", "site-packages"))

if app_root not in sys.path:
    sys.path.append(app_root)

os.environ.setdefault("UVCDAT_ANONYMOUS_LOG", "false")
os.environ.setdefault("HOME", "/var/www")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ea.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
