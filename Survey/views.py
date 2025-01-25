from django.shortcuts import render

from Survey.models import Client, Surveyor, Payment


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
    payments = Payment.objects.all()
    context = {
        'payments': payments,
    }
    return render(request, 'payments.html', context)


def registered_surveyor(request):
    return render(request,'registered_surveyor.html')


def messages(request):
    return render(request,'messages.html')


def new_payment(request):
    return render(request, 'new_payment.html')


def surveyor_view_details(request, object_id):
    surveyor= get_object_or_404(Surveyor, id=object_id)
    return render(request, 'surveyor_view_details.html', {'surveyor': surveyor})

def payment_details(request, object_id):
    payment = get_object_or_404(Payment, id=object_id)
    context = {
        'payment': payment,
    }
    return render(request, 'payment_details.html', context)