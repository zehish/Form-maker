#!/usr/bin/env python
"""
Utility script for administrative tasks.

This file is used to manage the Django project via the command line.  It is
generated manually for this project since we cannot run ``django-admin
startproject`` in this environment.  To use it in your own environment you
should install Django and run commands like::

    python manage.py runserver
    python manage.py makemigrations
    python manage.py migrate

See the Django documentation for more details.
"""
import os
import sys


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_forms.settings')
    try:
        from django.core.management import execute_from_command_line  # type: ignore
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()