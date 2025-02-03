from django.db import models
from django.http import request
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

MOBILE_SASA_API_URL = "https://api.mobilesasa.com/v1/send-message"
MOBILE_SASA_API_KEY = "api_key_here"


# Title Transfer Types
class TitleTransferTypes(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Title Transfer Type"
        verbose_name_plural = "Title Transfer Types"

    def __str__(self):
        return self.name

# Title Process
class TitleProcess(models.Model):
    type = models.ForeignKey(
        TitleTransferTypes,
        on_delete=models.SET_NULL,
        null=True,
        related_name="processes",
    )
    process = models.CharField(max_length=100)
    message = models.TextField(default="Your process is now in this stage. Thank you!")

    class Meta:
        ordering = ['id']
        verbose_name = "Title Process"
        verbose_name_plural = "Title Processes"

    def __str__(self):
        return f"{self.type.name if self.type else 'No Type'} - {self.process}"


# Client Model
class Client(models.Model):
    SERVICE_CHOICES = [
        ("land_survey", "Land Survey"),
        ("title_search", "Title Search"),
        ("land_transfer", "Land Transfer"),
        ("subdivision", "Subdivision"),
    ]

    PROCESS_CHOICES = [
        ("initial_submission", "Initial Submission"),
        ("registry_processing", "Registry Processing"),
        ("approval_verification", "Approval & Verification"),
        ("ready_for_collection", "Title Ready for Collection"),
    ]

    username = models.CharField(max_length=100, unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    join_date = models.DateTimeField(default=timezone.now)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, default='land_survey')
    process = models.CharField(max_length=50, choices=PROCESS_CHOICES, default='initial_submission')

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['username']
        db_table = 'clients'

# Automatically Set Initial Process for Clients
@receiver(post_save, sender=Client)
def set_initial_process(sender, instance, created, **kwargs):
    if created and instance.service:
        first_process = TitleProcess.objects.filter(type=instance.service).first()
        if first_process:
            instance.process = first_process
            instance.save()
            send_mobile_sasa_message(instance, first_process)

def send_mobile_sasa_message(client, message):
    payload = {
        "apiKey": MOBILE_SASA_API_KEY,
        "phone": client.phone,
        "message": message,
    }
    try:
        response = request.post(MOBILE_SASA_API_URL, json=payload)
        response_data = response.json()
        if response.status_code == 200 and response_data.get("success"):
            print(f"Message sent successfully to {client.phone}")
        else:
            print(f"Failed to send message: {response_data.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"Error while sending message: {e}")

# Surveyor Model
class Surveyor(models.Model):
    username = models.CharField(max_length=100, unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    action = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=200, default="inactive")
    join_date = models.DateTimeField(default=timezone.now)
    is_registered = models.BooleanField(default=False)
    is_serving = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        verbose_name = 'Surveyor'
        verbose_name_plural = 'Surveyors'
        ordering = ['username']
        db_table = 'surveyors'

@receiver(post_save, sender=Surveyor)
def set_default_action_and_status(sender, instance, created, **kwargs):
    if created:
        if instance.is_registered and instance.is_serving:
            instance.status = "active"
        else:
            instance.status = "inactive"

        instance.action = mark_safe(
            f'<a href="{reverse("surveyor_view_details", args=[instance.id])}" class="btn btn-outline-dark btn-sm">View Details</a>'
        )
        instance.save()

# Payment Model
class Payment(models.Model):
    client_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    amount = models.IntegerField()
    transaction_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=200, default="waiting for approval")
    action = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.client_name

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['client_name']
        db_table = 'payments'

@receiver(post_save, sender=Payment)
def set_default_action(sender, instance, created, **kwargs):
    if created:
        instance.action = mark_safe(
            f'<a href="{reverse("payment_details", args=[instance.id])}" class="btn btn-outline-dark btn-sm">Check Status</a>'
        )
        instance.save()

STATUS_CHOICES = [
    ("registry_processing", "Registry Processing"),
    ("approval_verification", "Approval and Verification"),
    ("ready_for_collection", "Title Deed Ready for Collection"),
]

class TitleDocument(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="documents")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="registry_processing")
    pdf_file = models.FileField(upload_to="title_documents/")
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.client.firstname} {self.client.lastname} - {self.status}"

    class Meta:
        verbose_name = "Title Document"
        verbose_name_plural = "Title Documents"
        ordering = ['-uploaded_at']

@receiver(post_save, sender=TitleDocument)
def notify_client_on_upload(sender, instance, created, **kwargs):
    if created:
        message = f"Dear {instance.client.firstname}, your title deed document has been uploaded with status: {instance.get_status_display()}."
        send_mobile_sasa_message(instance.client, message)
