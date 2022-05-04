from django.shortcuts import render


def home(request):

    template_name = 'home.html'
    context = {}

    return render(request, template_name, context)


def opportunities(request):

    template_name = 'opportunities.html'
    context = {}

    return render(request, template_name, context)
