"""
WSGI config for university_forms project.

This module contains the WSGI application used by Django's development server
and production servers alike.  It exposes a module-level variable
``application`` that can be used by WSGI servers such as Gunicorn.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/
"""
from __future__ import annotations

import os

from django.core.wsgi import get_wsgi_application  # type: ignore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_forms.settings')

application = get_wsgi_application()