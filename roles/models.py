
from django.db import models
# Create your models here.


class Permission(models.Model):
    module = models.CharField(max_length=100)
    action = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["module", "action"],
                name="unique_module_action"
            )
        ]

    def __str__(self):
        return f"{self.module} - {self.action}"


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="roles"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
