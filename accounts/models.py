from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)

    role = models.ForeignKey(
        'roles.Role',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='users'
    )


class UserSettings(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="user_settings"
    )
    email_notifications = models.BooleanField(default=True)
    theme = models.CharField(
        max_length=20,
        choices=[
            ("light", "Light"),
            ("dark", "Dark"),
        ],
        default="light"
    )

    def __str__(self):
        return f"Settings for {self.user.username}"
