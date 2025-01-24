from django.shortcuts import render

from Survey.models import Client, Surveyor


def dashboard(request):
    return render(request, 'admin-dash.html')


def surveyors(request):
    surveyors = Surveyor.objects.all()
    return render(request, 'surveyors.html',{'surveyors': surveyors})


def clients(request):
    clients = Client.objects.all()
    return render(request,'clients.html',{'clients': clients})


def payments(request):
    return render(request, 'payments.html')


def registered_surveyor(request):
    return render(request,'registered_surveyor.html')


def messages(request):
    return render(request,'messages.html')


def new_payment(request):
    return render(request, 'new_payment.html')