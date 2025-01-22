# =
#
#
from django.db import models
#
# from django.contrib.auth import get_user_model
#
from django.contrib.auth.models import AbstractUser
#
#
class CustomUser(AbstractUser):
    is_client = models.BooleanField(default=True)



# class Application(models.Model):
#     REQUEST_TYPES = [
#         ('title_deed', 'Title Deed Processing'),
#         ('subdivision', 'Subdivision Request'),
#         ('other', 'Other'),
#     ]
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('in_progress', 'In Progress'),
#         ('completed', 'Completed'),
#         ('rejected', 'Rejected'),
#     ]
#
#     client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')
#     request_type = models.CharField(max_length=50, choices=REQUEST_TYPES)
#     description = models.TextField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f"{self.client.username} - {self.request_type}"
#
#
# class AuditLog(models.Model):
#     ACTION_CHOICES = [
#         ('application_submitted', 'Application Submitted'),
#         ('document_uploaded', 'Document Uploaded'),
#         ('payment_made', 'Payment Made'),
#         ('status_updated', 'Status Updated'),
#         ('other', 'Other'),
#     ]
#
#     user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
#     action = models.CharField(max_length=50, choices=ACTION_CHOICES)
#     details = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.user.username if self.user else 'System'} - {self.action} at {self.timestamp}"
# CustomUser = get_user_model()
#

#
#

class Document(models.Model):
    type= models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


#title deed proceess and status /each process has different status
class Process(models.Model):
    name = models.CharField(max_length=50)

class Status(models.Model):
    status_process = models.ForeignKey('Process',on_delete=models.CASCADE ,related_name='process')
    name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


#every status is paid separately
class Payment(models.Model):
    reference = models.ForeignKey('Status', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} for {self.reference}"


#client can have different land under processes i.e Transfer and Subdivision
class Client(models.Model):
    user_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    Email =  models.EmailField(blank=True, null=True,unique=True)
    Phone =  models.CharField(max_length=50,unique=True)
    process = models.ManyToManyField('Process',related_name='process')

#Reciept after every paments
class Reciept(models.Model):
    client = models.ManyToManyField('Client',related_name='receipts').......

