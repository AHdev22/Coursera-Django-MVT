from django import forms
from django.contrib.auth.models import User

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email']  # leave phone in profile if you have Profile model
    
    def clean(self):
        # Optional: do not enforce password match in backend
        cleaned_data = super().clean()
        return cleaned_data
