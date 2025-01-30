"""
URL configuration for LandSurveyAgency project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from Survey import views
from Survey.views import client_view_details, client_dashboard

urlpatterns = [

    path('admin/', admin.site.urls),

path('', views.dashboard, name='dashboard'),
path('surveyors', views.surveyors, name='surveyors'),
path('clients', views.clients, name='clients'),
path('payments', views.payments, name='payments'),
path('new_payment', views.new_payment, name='new_payment'),
path('registered_surveyor', views.registered_surveyor, name='register_surveyor'),
path('messages', views.messages, name='messages'),
path('surveyors/surveyor_details<int:object_id>', views.surveyor_view_details, name='surveyor_view_details'),

path('clients/client_details<int:object_id>', views.client_view_details, name='client_view_details'),
    path('payments/payment_details/<int:object_id>/', views.payment_details, name='payment_details'),

path("client-dashboard/", client_dashboard, name="client_dashboard"),
]

