from django.shortcuts import render


def dashboard(request):
    return render(request, 'admin-dash.html')


def surveyors(request):
    return None


def clients(request):
    return None


def payments(request):
    return None


def registered_surveyor(request):
    return None


def messages(request):
    return None


def new_payment(request):
    return None