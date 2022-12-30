from django import forms
from django.db import models
from django.forms import ModelForm

from .models import registrationForm


class registrationForms(ModelForm):
    class Meta:
        model = registrationForm
        fields = ["userName", "firstName", "lastName", "email", "password"]
