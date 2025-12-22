"""
Views for the forms application.

This module implements both the public facing views used by respondents to
answer forms and the administrative interface used by the site owner to
create and manage forms.  The administrative interface is intentionally
simple and provided entirely in Persian.  Public forms are presented in
English with a footer credit to Zanjan University.
"""
from __future__ import annotations

import json
import uuid
import csv

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import translation
from django.utils.text import slugify

from .models import Answer, Choice, Form, Question, Response


def custom_login(request: HttpRequest) -> HttpResponse:
    """
    Render the login page and authenticate the user.

    The admin interface is protected by authentication.  This view
    displays a simple Persian login form and processes credentials
    submitted via POST.  Upon successful authentication the user is
    redirected to the dashboard.  If the credentials are invalid an
    error message is shown.
    """
    # Always activate Persian for the admin interface
    translation.activate('fa')
    if request.user.is_authenticated:
        return redirect('formsapp:dashboard')

    error: str | None = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('formsapp:dashboard')
        else:
            error = 'نام کاربری یا رمز عبور نادرست است.'  # Persian for "Invalid username or password."

    return render(request, 'admin/login.html', {'error': error})


@login_required(login_url='formsapp:login')
def dashboard(request: HttpRequest) -> HttpResponse:
    """
    Display the admin dashboard listing all forms.

    Authenticated administrators see a list of existing forms, each with
    options to view responses, export data, and share the form with
    respondents.  There is also a link to create a new form.  The page
    uses Persian throughout.
    """
    translation.activate('fa')
    forms = Form.objects.all().order_by('-created_at')
    return render(request, 'admin/dashboard.html', {'forms': forms})


@login_required(login_url='formsapp:login')
def create_form(request: HttpRequest) -> HttpResponse:
    """
    Create a new form along with its questions and choices.

    The form creation page allows the administrator to enter a title and
    dynamically add questions of type short answer or multiple choice.  The
    posted payload contains a JSON blob describing the questions.  After
    saving the data to the database a shareable slug is generated and the
    administrator is redirected to the dashboard with a success message.
    """
    translation.activate('fa')
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        form_data = request.POST.get('form_data')
        if not title or not form_data:
            messages.error(request, 'عنوان و داده‌های فرم الزامی هستند.')
            return redirect('formsapp:create_form')
        try:
            data = json.loads(form_data)
        except json.JSONDecodeError:
            messages.error(request, 'داده‌های ارسال شده نامعتبر هستند.')
            return redirect('formsapp:create_form')
        # Generate a unique slug using a combination of title and random suffix
        base_slug = slugify(title)
        slug = base_slug
        # Ensure the slug is unique
        counter = 1
        while Form.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        # Create the form
        form_obj = Form.objects.create(title=title, slug=slug, published=True)
        # Iterate through questions and create them
        questions_data = data.get('questions', [])
        for idx, q in enumerate(questions_data):
            q_text = q.get('text', '').strip()
            q_type = q.get('type')
            choices = q.get('choices', [])
            if not q_text or q_type not in (Question.TEXT, Question.MULTIPLE_CHOICE):
                continue
            question = Question.objects.create(
                form=form_obj,
                text=q_text,
                question_type=q_type,
                order=idx,
            )
            if q_type == Question.MULTIPLE_CHOICE:
                for choice_text in choices:
                    ct = choice_text.strip()
                    if ct:
                        Choice.objects.create(question=question, text=ct)
        messages.success(request, 'فرم با موفقیت ایجاد شد.')
        return redirect('formsapp:dashboard')
    return render(request, 'admin/create_form.html')


def display_form(request: HttpRequest, slug: str) -> HttpResponse:
    """
    Display a published form for respondents and handle submissions.

    The form page is presented in English.  When a respondent submits
    answers via POST the response and answers are saved to the database.
    After submission a thank you page is rendered.
    """
    # Activate English for the public interface
    translation.activate('en')
    form_obj = get_object_or_404(Form, slug=slug, published=True)
    if request.method == 'POST':
        # Create a response entry
        response_obj = Response.objects.create(form=form_obj)
        for question in form_obj.questions.all():
            field_name = f"question_{question.id}"
            value = request.POST.get(field_name)
            if question.question_type == Question.TEXT:
                Answer.objects.create(
                    response=response_obj,
                    question=question,
                    text=value or '',
                )
            else:
                # Multiple choice: value is choice id
                choice_obj = None
                text_value = ''
                if value:
                    try:
                        choice_obj = Choice.objects.get(id=int(value), question=question)
                        text_value = choice_obj.text
                    except (ValueError, Choice.DoesNotExist):
                        text_value = value
                Answer.objects.create(
                    response=response_obj,
                    question=question,
                    choice=choice_obj,
                    text=text_value,
                )
        return render(request, 'thanks.html', {'form': form_obj})

    return render(request, 'form.html', {'form': form_obj})


@login_required(login_url='formsapp:login')
def view_responses(request: HttpRequest, form_id: int) -> HttpResponse:
    """
    Display all responses to a given form.

    The page shows a simple table with one row per response and one column
    per question.  Because questions can change over time the export
    functions should be used for serious data analysis.
    """
    translation.activate('fa')
    form_obj = get_object_or_404(Form, id=form_id)
    responses = form_obj.responses.all().order_by('-submitted_at')
    questions = list(form_obj.questions.all())
    # Build a table of answers keyed by response
    table: list[tuple[Response, list[str]]] = []
    for response in responses:
        row: list[str] = []
        for question in questions:
            ans = response.answers.filter(question=question).first()
            if ans:
                row.append(ans.choice.text if ans.choice else ans.text)
            else:
                row.append('')
        table.append((response, row))
    return render(request, 'admin/responses.html', {
        'form': form_obj,
        'questions': questions,
        'table': table,
    })


@login_required(login_url='formsapp:login')
def export_responses_csv(request: HttpRequest, form_id: int) -> HttpResponse:
    """
    Export responses to a CSV file.

    The generated file contains one header row with question texts followed
    by one row per response.  Each cell contains either the selected
    choice text or the free text answer.
    """
    form_obj = get_object_or_404(Form, id=form_id)
    questions = list(form_obj.questions.all())
    responses = form_obj.responses.all().order_by('submitted_at')
    # Create the CSV file in memory
    response = HttpResponse(content_type='text/csv')
    filename = slugify(form_obj.title) or 'form'
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
    writer = csv.writer(response)
    # Header row
    header = ['Submitted At'] + [q.text for q in questions]
    writer.writerow(header)
    for resp in responses:
        row = [resp.submitted_at.isoformat()]
        for q in questions:
            ans = resp.answers.filter(question=q).first()
            if ans:
                row.append(ans.choice.text if ans.choice else ans.text)
            else:
                row.append('')
        writer.writerow(row)
    return response


@login_required(login_url='formsapp:login')
def export_responses_xlsx(request: HttpRequest, form_id: int) -> HttpResponse:
    """
    Export responses to an Excel file (.xlsx).

    Requires the openpyxl library.  If openpyxl is unavailable an error
    message is displayed prompting the administrator to install it.
    """
    form_obj = get_object_or_404(Form, id=form_id)
    questions = list(form_obj.questions.all())
    responses_qs = form_obj.responses.all().order_by('submitted_at')
    try:
        from openpyxl import Workbook  # type: ignore
    except ImportError:
        messages.error(request, 'کتابخانه openpyxl نصب نشده است. لطفاً قبل از استفاده، آن را نصب کنید.')
        return redirect('formsapp:view_responses', form_id=form_id)
    wb = Workbook()
    ws = wb.active
    ws.title = 'Responses'
    # Header row
    ws.append(['Submitted At'] + [q.text for q in questions])
    for resp in responses_qs:
        row = [resp.submitted_at.isoformat()]
        for q in questions:
            ans = resp.answers.filter(question=q).first()
            if ans:
                row.append(ans.choice.text if ans.choice else ans.text)
            else:
                row.append('')
        ws.append(row)
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = slugify(form_obj.title) or 'form'
    response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
    wb.save(response)
    return response