"""
WSGI config for ea project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

app_root = os.path.dirname(os.path.dirname(__file__))
if app_root not in sys.path:
	sys.path.append(app_root)

os.environ.setdefault("UVCDAT_ANONYMOUS_LOG", "false")
os.environ.setdefault("HOME", "/var/www")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ea.settings")

print 'sys.path: ' + str(sys.path)


application = get_wsgi_application()

