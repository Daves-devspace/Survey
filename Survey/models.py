from django.db import models

# Create your models here.
class Client(models.Model):
    username = models.CharField(max_length=100,unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    action = models.CharField(max_length=200, default="view details")  # Action for the client
    status = models.CharField(max_length=200, default="waiting for approval")

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['username']
        db_table = 'clients'

class Surveyor(models.Model):
    username = models.CharField(max_length=100, unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    status = models.CharField(max_length=200, default="active")  # Surveyor status is always active

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Surveyor'
        verbose_name_plural = 'Surveyors'
        ordering = ['username']
        db_table = 'surveyors'

class Transaction(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    surveyor = models.ForeignKey(Surveyor, on_delete=models.CASCADE, related_name='transactions')
    status = models.CharField(max_length=200)
    action = models.CharField(max_length=200)
    transaction_date = models.DateTimeField(auto_now_add=True)

    @property
    def __str__(self):
        return f"Transaction {self.id} - {self.client.username} & {self.surveyor.username}"

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-transaction_date']
        db_table = 'transactions'

class Payment(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    merchant_request_id = models.CharField(max_length=100)
    checkout_request_id = models.CharField(max_length=100)
    code = models.CharField(max_length=30, null=True)
    amount = models.IntegerField()
    status = models.CharField(max_length=20, default="Cancelled")
    transaction_date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100, default="Check Status")

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-transaction_date']
        db_table = 'payments'
    def __str__(self):
        return f"{self.merchant_request_id} - {self.code} - {self.amount} - {self.status}"