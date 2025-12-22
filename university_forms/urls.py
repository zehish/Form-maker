"""
URL configuration for the university_forms project.

The ``urlpatterns`` list routes URLs to views.  For more information please
see:
    https://docs.djangoproject.com/en/stable/topics/http/urls/

This project uses a custom application ``formsapp`` to handle form creation
and response submission.  The built-in Django admin site is not used for
form management but remains available at the ``/djadmin/`` path for debugging
and inspection.  The custom admin interface for creating forms is exposed
at ``/admin/``.
"""
from __future__ import annotations

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # The built‑in Django admin site is mounted under /djadmin/ so as not to
    # clash with the custom form management admin interface.  You can remove
    # this in production if you do not wish to expose the built‑in admin.
    path('djadmin/', admin.site.urls),
    # Mount our forms application.
    path('', include('formsapp.urls')),
]