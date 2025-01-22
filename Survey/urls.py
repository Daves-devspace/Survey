from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),
    path('submit-application/', views.submit_application, name='submit_application'),
    path('upload-document/<int:application_id>/', views.upload_document, name='upload_document'),
    path('make-payment/<int:application_id>/', views.make_payment, name='make_payment'),
    path('track-process/<int:application_id>/', views.track_process, name='track_process'),
    path('dashboard/', views.client_dashboard, name='client_dashboard'),
]
