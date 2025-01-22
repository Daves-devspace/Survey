from django.contrib import messages
from django.db import models
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, DocumentForm
from .forms import ApplicationForm
from .models import Application, AuditLog, CustomUser, Payment


def homepage(request):
    return render(request, 'client_dashboard/home.html')
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'client_dashboard/register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'client_dashboard/login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'client_dashboard/dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def submit_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.client = request.user
            application.save()
            # Log the action
            AuditLog.objects.create(
                user=request.user,
                action='application_submitted',
                details=f"Application {application.id} submitted."
            )
            return redirect('client_dashboard')
    else:
        form = ApplicationForm()
    return render(request, 'client_dashboard/submit_application.html', {'form': form})
@login_required
def upload_document(request, application_id):
    application = Application.objects.get(id=application_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.application = application
            document.save()
            # Log the action
            AuditLog.objects.create(
                user=request.user,
                action='document_uploaded',
                details=f"Document uploaded for application {application.id}."
            )
            return redirect('client_dashboard')
    else:
        form = DocumentForm()
    return render(request, 'client_dashboard/upload_document.html', {'form': form, 'application': application})






@login_required
def make_payment(request, application_id):
    application = Application.objects.get(id=application_id)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        transaction_id = request.POST.get('transaction_id')
        # Simulate payment processing
        Payment.objects.create(
            application=application,
            amount=amount,
            payment_method='M-Pesa',
            transaction_id=transaction_id
        )
        # Log the action
        AuditLog.objects.create(
            user=request.user,
            action='payment_made',
            details=f"Payment made for application {application.id}."
        )
        return redirect('client_dashboard')
    return render(request, 'client_dashboard/make_payment.html', {'application': application})
@login_required
def track_process(request, application_id):
    application = Application.objects.get(id=application_id)
    return render(request, 'client_dashboard/track_process.html', {'application': application})

@login_required
def client_dashboard(request):
    applications = Application.objects.filter(client=request.user)
    # Example notification
    messages.info(request, 'You have 2 pending applications.')
    return render(request, 'client_dashboard/dashboard.html', {'applications': applications})
