from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime

from .models import RegisteredEmail, Support, Message, Vacancy
from .forms import MessageForm


def home(request):

    template_name = 'home.html'
    context = {}

    return render(request, template_name, context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def inbox(request):
    if 'q' in request.GET:
        q = request.GET['q']
        messages = Message.objects.filter(
            Q(name__icontains=q) | Q(email__icontains=q) |
            Q(subject__icontains=q) | Q(body__icontains=q) |
            Q(status__icontains=q))
    else:
        messages = Message.objects.all()

    total_messages = Message.objects.count()
    read_messages = Message.objects.filter(status=Message.READ).count()
    unread_messages = Message.objects.filter(status=Message.PENDING).count()
    now = datetime.now().date()
    today = Message.objects.filter(created__gt=now).count()

    template_name = 'inbox.html'
    context = {
        'messages': messages,
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


def backend_email(request):

    template_name = 'backend_email.html'
    context = {}

    return render(request, template_name, context)


def support(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Support.objects.filter(email=email).exists():
            messages.info(request, ".")
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

    template_name = 'support.html'
    context = {}

    return render(request, template_name, context)


def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your message has been sent to us.")
            return redirect("home")
        # if request.POST.get('message'):
        #     message = Message()
        #     message.body = request.POST.get('message')
        #     message.save()
        #     messages.success(
        #         request, "Your message has been sent to us.")
        #     return redirect("home")
    else:
        form = MessageForm()
    return render(request, 'home.html', {'form': form})


# Destroy session upon logout
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def dashboard(request):
    total_candidates = RegisteredEmail.objects.all().count()
    vacancy = Vacancy.objects.first()

    template_name = 'dashboard.html'
    context = {
        'total_candidates': total_candidates,
        'vacancy': vacancy,
    }

    return render(request, template_name, context)


def faq(request):

    template_name = 'faq.html'
    context = {}

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
    # template_name = 'edit_vacancy.html'
    # context = {}

    # return render(request, template_name, context)


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
