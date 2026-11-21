from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from jobnest_app.models import Job


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields =['username','email','password1','password2']


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields=['title','company','location','salary','description']