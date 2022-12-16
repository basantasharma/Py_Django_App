from django.contrib import admin
from .models import registrationForm
@admin.register(registrationForm)
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("firstName", "lastName")
#admin.site.register(registrationForm)