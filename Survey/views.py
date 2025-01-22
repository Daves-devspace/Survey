from django.contrib import messages
from django.db import models
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required



def homepage(request):
    return render(request, 'Admin/admin-dash.html')


def Client_list(request):
    return render(request,'Admin/Clients.html')


def Survey_list(request):
    return render(request,'Admin/surveyor.html')


def Client_payments(request):
    return render(request,'Admin/Payments.html')


def Office_documents(request):
    return render(request,'Admin/documents.html')