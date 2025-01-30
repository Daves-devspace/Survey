from django import forms
from .models import Client, TitleProcess, TitleDocument

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['firstname', 'lastname', 'email', 'phone', 'service']  # Exclude 'process'

    def save(self, commit=True):
        client = super().save(commit=False)
        if not client.process and client.service:
            first_process = TitleProcess.objects.filter(type=client.service).first()
            if first_process:
                client.process = first_process
        if commit:
            client.save()
        return client

# ✅ New: Title Document Upload Form
class TitleDocumentForm(forms.ModelForm):
    class Meta:
        model = TitleDocument
        fields = ['client', 'status', 'pdf_file']  # Include all relevant fields

    def save(self, commit=True):
        document = super().save(commit=False)
        if commit:
            document.save()
        return document
