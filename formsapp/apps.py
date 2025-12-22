"""
Configuration for the formsapp application.

When the application is ready we ensure that the preconfigured admin user
exists.  Because we cannot run ``createsuperuser`` in this environment we
bootstrap the admin credentials (username ``university`` and password
``14042026``) programmatically.  In a production environment you should
change these credentials and rely on Django's built-in authentication
mechanisms to manage user accounts.
"""
from __future__ import annotations

from django.apps import AppConfig
from django.contrib.auth import get_user_model


class FormsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'formsapp'
    verbose_name = "فرم‌ها"

    def ready(self) -> None:
        """
        Avoid executing database queries during app initialization.

        In earlier versions of this project the admin user was
        automatically created in this method, but that can cause
        ``OperationalError`` exceptions if migrations have not yet been
        applied.  To create the administrative user, run::

            python manage.py createsuperuser --username university --email admin@example.com

        and set the password to ``14042026`` when prompted.  This ensures
        that the database tables exist before the user is created.
        """
        return