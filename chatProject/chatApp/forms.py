from .models import registrationForm
from django import forms
from django.db import models
from django.forms import ModelForm

class registrationForms(ModelForm):
    class Meta:
        fields = ["userName","firstName", "lastName", "email", "password"]