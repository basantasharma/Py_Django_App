from django.db import models

# Create your models here.
class registrationForm(models.Model):
    userName = models.CharField(max_length=30, null=True)
    firstName = models.CharField(max_length=30, null=True)
    lastName = models.CharField(max_length=30, null=True)
    email = models.CharField(max_length=30, null=True)
    password = models.CharField(max_length=50, default='Chat@pp123')
    def __str__(self):
        return self.firstName + ' ' + self.lastName + ' ' + self.userName + ' ' + self.email + ' ' + self.password