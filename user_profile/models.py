from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )
    nickname = models.CharField(max_length=20, unique=True)
    profile_image = models.ImageField(
        upload_to="user_profile/profile", blank=True, null=True
    )
    description = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.nickname
