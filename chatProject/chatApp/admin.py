from django.contrib import admin
from .models import registrationForm
@admin.register(registrationForm)
# @admin.register(friend_list)

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("userName","firstName", "lastName", "email", "password")
    #admin.site.register(registrationForm)