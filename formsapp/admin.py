"""
Admin registrations for formsapp models.

Although the application provides its own custom management interface for
creating and managing forms, the models are registered with the Django admin
for convenience.  Access the Django admin at ``/djadmin/``.  The admin
interface may be useful for debugging or ad‑hoc data inspection.
"""
from __future__ import annotations

from django.contrib import admin
from .models import Answer, Choice, Form, Question, Response


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'published')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'form', 'question_type', 'order')
    list_filter = ('form',)
    ordering = ('form', 'order')


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question')
    list_filter = ('question',)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('form', 'submitted_at')
    list_filter = ('form',)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('response', 'question', 'text', 'choice')
    list_filter = ('question',)