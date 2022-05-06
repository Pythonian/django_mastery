from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.conf import settings


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
        fullname = request.POST.get('fullname')
        age = request.POST.get('age')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        experience = request.POST.get('experience')
        skills = request.POST.get('skills')

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
