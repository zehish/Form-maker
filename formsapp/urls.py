"""
URL patterns for the forms application.

This module defines routes for both the public and administrative portions
of the application.  Administrative URLs all begin with ``/admin/`` and
require authentication.  The built‑in Django authentication views are
leveraged for login and logout where appropriate.
"""
from __future__ import annotations

from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'formsapp'

urlpatterns = [
    # Public form display and submission
    path('form/<slug:slug>/', views.display_form, name='display_form'),

    # Custom admin panel
    path('admin/', views.dashboard, name='dashboard'),
    path('admin/create/', views.create_form, name='create_form'),
    path('admin/form/<int:form_id>/responses/', views.view_responses, name='view_responses'),
    path('admin/form/<int:form_id>/export/csv/', views.export_responses_csv, name='export_csv'),
    path('admin/form/<int:form_id>/export/xlsx/', views.export_responses_xlsx, name='export_xlsx'),

    # Form management actions
    path('admin/form/<int:form_id>/delete/', views.delete_form, name='delete_form'),
    path('admin/form/<int:form_id>/archive/', views.archive_form, name='archive_form'),

    # Login and logout using Django's built-in auth views but with custom templates
    path('admin/login/', views.custom_login, name='login'),
    path('admin/logout/', auth_views.LogoutView.as_view(next_page='formsapp:login'), name='logout'),
]