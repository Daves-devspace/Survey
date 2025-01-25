from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils import timezone
# Create your models here.
class Client(models.Model):
    username = models.CharField(max_length=100, unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    action = models.CharField(max_length=200, blank=True)  # Allow blank for default value
    status = models.CharField(max_length=200, default="waiting for approval")
    join_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['username']
        db_table = 'clients'

# Signal to set the default action button
@receiver(post_save, sender=Client)
def set_default_action(sender, instance, created, **kwargs):
    if created and not instance.action:  # Set default value only for new instances
        instance.action = mark_safe(
            f'<a href="{reverse("client_view_details", args=[instance.id])}" class="btn btn-outline-dark btn-sm">View Details</a>'
        )
        instance.save()


class Surveyor(models.Model):
    username = models.CharField(max_length=100, unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    action = models.CharField(max_length=200, blank=True)  # Allow blank for default value
    status = models.CharField(max_length=200, default="inactive")  # Default status is "inactive"
    join_date = models.DateTimeField(default=timezone.now)
    is_registered = models.BooleanField(default=False)  # Track if the surveyor is registered
    is_serving = models.BooleanField(default=False)  # Track if the surveyor is serving in the company

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        verbose_name = 'Surveyor'
        verbose_name_plural = 'Surveyors'
        ordering = ['username']
        db_table = 'surveyors'
# Signal to set the default action button and status
@receiver(post_save, sender=Surveyor)
def set_default_action_and_status(sender, instance, created, **kwargs):
    if created:  # Only for new instances
        # Set the status based on registration and serving status
        if instance.is_registered and instance.is_serving:
            instance.status = "active"
        else:
            instance.status = "inactive"

        # Set the default action button
        instance.action = mark_safe(
            f'<a href="{reverse("surveyor_view_details", args=[instance.id])}" class="btn btn-outline-dark btn-sm">View Details</a>'
        )

        # Save the instance to update the fields
        instance.save()

class Payment(models.Model):
    client_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    amount = models.IntegerField()
    transaction_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=200, default="waiting for approval")
    action = models.CharField(max_length=200, blank=True)  # Allow blank for default value

    def __str__(self):
        return self.client_name

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['client_name']
        db_table = 'payments'

# Signal to set the default action button
@receiver(post_save, sender=Payment)
def set_default_action(sender, instance, created, **kwargs):
    if created:  # Only for new instances
        instance.action = mark_safe(
            f'<a href="{reverse("payment_details", args=[instance.id])}" class="btn btn-outline-dark btn-sm">Check Status</a>'
        )
        instance.save()