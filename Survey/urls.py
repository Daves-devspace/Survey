from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('clients/', views.Client_list, name='clients'),
    path('survey/', views.Survey_list, name='survey'),
    path('payments/', views.Client_payments, name='payments'),
    path('documents/', views.Office_documents, name='documents'),

]
