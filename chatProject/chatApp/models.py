from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class registrationForm(models.Model):
    userName = models.CharField(max_length=30, null=True)
    firstName = models.CharField(max_length=30, null=True)
    lastName = models.CharField(max_length=30, null=True)
    email = models.CharField(max_length=30, null=True)
    password = models.CharField(max_length=50, default="Chat@pp123")

    def __str__(self):
        return (
            self.firstName
            + " "
            + self.lastName
            + " "
            + self.userName
            + " "
            + self.email
            + " "
            + self.password
        )


class user_friend_requests(models.Model):
    from_users = models.ForeignKey(
        User, related_name="from_users_id", on_delete=models.CASCADE
    )
    to_users = models.ForeignKey(
        User, related_name="to_users_id", on_delete=models.CASCADE
    )
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user_friend_requests"
