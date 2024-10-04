from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        CUSTOMER = "CUSTOMER", "Customer"

    role = models.CharField(max_length=50, choices=Role.choices)
    location = models.CharField(max_length=255, blank=True)  # Field to store the user's location
    verification_code = models.CharField(max_length=32, blank=True)  # Field to store the verification code
    is_verified = models.BooleanField(default=False)


