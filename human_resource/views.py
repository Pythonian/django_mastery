from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

from .models import RegisteredEmail, Support


def home(request):

    template_name = 'home.html'
    context = {}

    return render(request, template_name, context)


def opportunities(request):

    template_name = 'opportunities.html'
    context = {}

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
            return HttpResponseRedirect('/')

    template_name = 'support.html'
    context = {}

    return render(request, template_name, context)


# Destroy session upon logout
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def dashboard(request):

    template_name = 'dashboard.html'
    context = {}

    return render(request, template_name, context)
