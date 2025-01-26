from django import forms
from .models import Client, TitleProcess


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'service']  # Exclude 'process'

    def save(self, commit=True):
        client = super().save(commit=False)
        if not client.process and client.service:
            first_process = TitleProcess.objects.filter(type=client.service).first()
            if first_process:
                client.process = first_process
        if commit:
            client.save()
        return client
