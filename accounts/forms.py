from django import forms
from .models import Profile


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'phone']
