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

from django.shortcuts import get_object_or_404, render
from .models import Client

def client_view_details(request, object_id):
    client = get_object_or_404(Client, id=object_id)
    return render(request, 'client_view_details.html', {'client': client})

def payments(request):
    return render(request, 'payments.html')


def registered_surveyor(request):
    return render(request,'registered_surveyor.html')


def messages(request):
    return render(request,'messages.html')


def new_payment(request):
    return render(request, 'new_payment.html')