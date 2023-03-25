from datetime import datetime

import pdfkit
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.views.decorators.cache import cache_control

from .forms import CandidateForm, GroupChatForm, MessageCandidate, MessageForm, ReplyMessage
from .models import Candidate, GroupChat, Message, RegisteredEmail, Support, Vacancy
from .utils import mk_paginator


def home(request):

    template_name = 'home.html'
    context = {'form': MessageForm()}

    return render(request, template_name, context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def inbox(request):
    if 'q' in request.GET:
        q = request.GET['q']
        all_messages = Message.objects.filter(
            Q(name__icontains=q) | Q(email__icontains=q) |
            Q(subject__icontains=q) | Q(body__icontains=q) |
            Q(status__icontains=q))
    else:
        all_messages = Message.objects.all()

    total_messages = Message.objects.count()
    read_messages = Message.objects.filter(status=Message.READ).count()
    unread_messages = Message.objects.filter(status=Message.PENDING).count()
    now = datetime.now().date()
    today = Message.objects.filter(created__gt=now).count()

    template_name = 'inbox.html'
    context = {
        'all_messages': all_messages,
        'today': today,
        'total_messages': total_messages,
        'read_messages': read_messages,
        'unread_messages': unread_messages,
    }

    return render(request, template_name, context)


def opportunities(request):
    vacancy = Vacancy.objects.first()

    template_name = 'opportunities.html'
    context = {'vacancy': vacancy}

    return render(request, template_name, context)


def frontend_email(request):
    if request.method == 'POST':

        email = request.POST['email']
        if RegisteredEmail.objects.filter(email=email).exists():
            messages.error(
                request, "You have already submitted your CV.")
            return HttpResponseRedirect('/opportunities/')
        else:
            fullname = request.POST.get('fullname')
            age = request.POST.get('age')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            experience = request.POST.get('experience')
            skills = request.POST.get('skills')

            candidate = RegisteredEmail()
            candidate.email = email
            candidate.save()

            template = loader.get_template('resume_form.txt')
            context = {
                'fullname': fullname,
                'age': age,
                'email': email,
                'phone': phone,
                'address': address,
                'experience': experience,
                'skills': skills,
            }
            message = template.render(context)
            email = EmailMultiAlternatives(
                "Frontend - Candidate",
                message,
                "Frontend Opportunity",
                [settings.EMAIL_HOST_USER]
            )
            email.content_subtype = 'html'
            file = request.FILES['file']
            email.attach(file.name, file.read(), file.content_type)
            email.send()
            messages.success(
                request, "Frontend resume sent successfully.")
            return HttpResponseRedirect("/")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def support(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Support.objects.filter(email=email).exists():
            messages.warning(request, ".")
            return HttpResponseRedirect('/support/')
        else:
            support = Support()
            message = request.POST.get('message')
            terms = request.POST.get('terms')
            person = request.POST.get('person')
            subject = request.POST.get('subject')
            email = request.POST.get('email')

            support.message = message
            support.terms = terms
            support.person = person
            support.subject = subject
            support.email = email
            support.status = Support.PENDING

            support.save()
            messages.success(request, "We will review your request")
            if request.user.is_authenticated:
                return redirect('dashboard')
            else:
                return redirect('home')

    vacancy = Vacancy.objects.first()

    template_name = 'support.html'
    context = {'vacancy': vacancy}

    return render(request, template_name, context)


def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your message has been sent to us.")
            return redirect("home")
    else:
        form = MessageForm()
    return render(request, 'home.html', {'form': form})


# Destroy session upon logout
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def dashboard(request):
    vacancy = Vacancy.objects.first()
    unread_messages = Message.objects.filter(status=Message.PENDING).count()

    template_name = 'dashboard.html'
    context = {
        'vacancy': vacancy,
        'unread_messages': unread_messages,
    }

    return render(request, template_name, context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def edit_vacancy(request):
    if request.method == 'POST':
        vacancy = Vacancy.objects.first()
        # vacancy = Vacancy.objects.get(id=request.POST.get('id'))
        if vacancy is not None:
            vacancy.frontend = request.POST.get('frontend')
            vacancy.design = request.POST.get('design')
            vacancy.backend = request.POST.get('backend')
            vacancy.devops = request.POST.get('devops')
            vacancy.save()
            messages.success(request, "Job vacancies updated.")
            return redirect("dashboard")
    else:
        return render(request, 'dashboard.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def edit_countdown(request):
    if request.method == 'POST':
        vacancy = Vacancy.objects.first()
        if vacancy is not None:
            vacancy.timer = request.POST.get('timer')
            vacancy.save()
            messages.success(request, "Countdown timer updated.")
            return redirect("dashboard")


@login_required
def message(request, pk):
    message = get_object_or_404(Message, pk=pk)

    from_email = settings.DEFAULT_FROM_EMAIL
    if request.method == 'POST':
        reply_form = ReplyMessage(request.POST, request.FILES)
        if reply_form.is_valid():
            subject = reply_form.cleaned_data['subject']
            body = reply_form.cleaned_data['body']
            to_email = message.email
            cc = reply_form.cleaned_data['cc']
            attachments = request.FILES.getlist('attachments')

            mail = EmailMessage(subject, body, from_email, [to_email], [cc])
            for file in attachments:
                mail.attach(file.name, file.read(), file.content_type)
            mail.send()
            messages.success(request, 'Reply sent successfully.')
            return redirect('inbox')
    else:
        reply_form = ReplyMessage()

    template_name = 'message.html'
    context = {'message': message, 'reply_form': reply_form}

    return render(request, template_name, context)


@login_required
def mark_as_read(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        message.status = message.READ
        message.save()
        messages.success(request, "Message marked as read.")
        return redirect('inbox')


# def waiting(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         if Waiting.objects.filter(email=email).exists():
#             messages.warning(request, "You have sent something")
#             return redirect('/waiting/')
#         else:
#             file = request.FILES['resume']
#             attach = FileSystemStorage()
#             resume_document = attach.save(file.name, file)

#             waiting = Waiting(
#                 job=request.POST.get('job'),
#                 email=request.POST.get('email'),
#                 message=request.POST.get('message'),
#                 resume=resume_document)
#             waiting.save()
#             messages.success(request, "Successful")
#             return redirect('/')
#     else:
#         return render(request, 'waiting.html')

############################################
#               CANDIDATES                 #
############################################

def candidate_create(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Your application form was sent to us successfully.")
            return redirect('application')
        else:
            messages.warning(
                request, "An error occured during the submission of your form. Please check below.")
    else:
        form = CandidateForm()

    return render(request, 'application.html', {'form': form})


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def candidate_list(request):
    if 'f' in request.GET:
        f = request.GET['f']
        candidates = Candidate.objects.filter(Q(job__iexact=f) |
            Q(gender__iexact=f) | Q(status=f))
    elif 'asc' in request.GET:
        candidates = Candidate.objects.order_by('firstname')
    elif 'desc' in request.GET:
        candidates = Candidate.objects.order_by('-firstname')
    elif 'q' in request.GET:
        q = request.GET['q']
        candidates = Candidate.objects.annotate(fullname=Concat('firstname', Value(' '), 'lastname')).filter(
            Q(fullname__icontains=q) | Q(firstname__icontains=q) | Q(lastname__icontains=q) |
            Q(email__icontains=q))
    else:
        candidates = Candidate.objects.all()

    total_candidates = candidates.count()
    fullstack_candidates = candidates.filter(job='FS-22').count()
    frontend_candidates = candidates.filter(job='FE-22').count()
    backend_candidates = candidates.filter(job='BE-22').count()

    candidates = mk_paginator(request, candidates, 15)

    context = {'candidates': candidates,
         'total_candidates': total_candidates,
         'fullstack_candidates': fullstack_candidates,
         'frontend_candidates': frontend_candidates,
         'backend_candidates': backend_candidates}

    return render(
        request, 'candidates.html', context)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def candidate_detail(request, id):
    candidate = get_object_or_404(Candidate, id=id)

    from_email = settings.DEFAULT_FROM_EMAIL
    if request.method == 'POST':
        message_form = MessageCandidate(request.POST)
        if message_form.is_valid():
            subject = message_form.cleaned_data['subject']
            body = message_form.cleaned_data['body']
            to_email = candidate.email
            
            mail = EmailMessage(subject, body, from_email, [to_email])
            mail.send()
            messages.success(request, 'Message sent successfully.')
            return redirect(candidate)
    else:
        message_form = MessageCandidate()

    template = 'candidate.html'
    context = {'candidate': candidate, 'message_form': message_form}

    return render(request, template, context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def candidate_delete(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    fullname = f'{candidate.firstname} {candidate.lastname}'
    candidate.delete()
    messages.success(request, f"Candidate: {fullname} successfully deleted.")
    return redirect('candidates')


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def export_to_pdf(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    cookies = request.COOKIES
    # Pass in the cookie dict to allow the pdf library access the restricted page
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
        'cookie': [
            ('csrftoken', cookies['csrftoken']),
            ('sessionid', cookies['sessionid'])
        ]
    }
    pdf_name = candidate.firstname + '_' + candidate.lastname + '.pdf'
    pdf = pdfkit.from_url('http://127.0.0.1:8000/pdf/' + str(candidate.id), False, options=options)
    # pdf = pdfkit.from_url('http://127.0.0.1:8000/candidate/' + str(c.id), False, options=options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-disposition'] = 'attachment; filename={}'.format(pdf_name)
    return response


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def generate_pdf(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    return render(request, 'pdf.html', {'candidate': candidate})


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def group_chat(request, id):
    candidate = get_object_or_404(Candidate, id=id)
    group_chat = GroupChat.objects.all().order_by('-created')
    users = User.objects.all()
    form = GroupChatForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('group_chat', id=candidate.id)
    return render(request, 'group_chat.html', {'form': form, 'group_chat': group_chat, 'users': users, 'candidate': candidate})


############################################
#               ERROR PAGES                #
############################################

def error_500(request):
    return render(request, '500.html')


def error_404(request, exception):
    return render(request, '404.html')


def autologout(request):
    logout(request)
    request.user = None
    # Pass the message in the HTML
    messages.info(request, "You have been automatically logged out. Your account is now secure!")
    return redirect('home')
