# from django import forms
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from .models import CustomUser, Application, Document
#
# # Existing User Forms
# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'email', 'password1', 'password2')
#
# class CustomAuthenticationForm(AuthenticationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'password')
#
# # Application Submission Form
# class ApplicationForm(forms.ModelForm):
#     class Meta:
#         model = Application
#         fields = ['request_type', 'description']
#         widgets = {
#             'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your request...'}),
#         }
#
# # Document Upload Form
# class DocumentForm(forms.ModelForm):
#     class Meta:
#         model = Document
#         fields = ['file']
#         widgets = {
#             'file': forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx,.jpg,.png'}),
#         }