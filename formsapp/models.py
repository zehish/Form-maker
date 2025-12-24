"""
Database models for the forms application.

The application is composed of several simple models that together
represent a form, its questions, available choices, and the responses
received from users.  Each form may have an arbitrary number of questions
in a specific order.  Questions can be either short answer (text) or
multiple choice.  For multiple choice questions there may be several
choices from which the respondent selects one.

Responses are stored along with their individual answers.  Answers may be
associated with a choice (for multiple choice questions) and/or contain
free text.
"""
from __future__ import annotations

from django.db import models


class Form(models.Model):
    """Represents a published form that people can answer."""

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    # A short description shown beneath the form title for respondents.  This field
    # can be left blank and is optional.  Administrators can use it to provide
    # additional context such as instructions or the purpose of the form.
    description = models.TextField(blank=True, null=True)
    # When a form is archived the administrative interface will hide its
    # responses.  Responses remain in the database but are no longer accessible
    # through the UI.  Administrators can toggle this flag via the dashboard.
    archived = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title


class Question(models.Model):
    """A question belonging to a form."""

    TEXT = 'text'
    MULTIPLE_CHOICE = 'mc'
    QUESTION_TYPES = [
        (TEXT, 'Short answer'),
        (MULTIPLE_CHOICE, 'Multiple choice'),
    ]

    form = models.ForeignKey(Form, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=1024)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default=TEXT)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self) -> str:
        return f"{self.text}"  # pragma: no cover


class Choice(models.Model):
    """A choice for a multiple choice question."""

    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.text


class Response(models.Model):
    """A single response to a form."""

    form = models.ForeignKey(Form, related_name='responses', on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Response to {self.form.title} at {self.submitted_at}"


class Answer(models.Model):
    """Stores an answer to a specific question within a response."""

    response = models.ForeignKey(Response, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    choice = models.ForeignKey(Choice, related_name='answers', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"Answer to {self.question.text}"