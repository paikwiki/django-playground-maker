import os
from django.db import migrations


def create_superuser(apps, schema_editor):
    User = apps.get_model("auth", "User")
    UserProfile = apps.get_model("user_profile", "UserProfile")

    password = os.getenv("SUPERUSER_PASSWORD", None)

    if not password:
        raise ValueError("SUPERUSER_PASSWORD environment variable is not set")

    user = User.objects.create_superuser(
        username="admin", email="admin@example.com", password=password
    )

    UserProfile.objects.create(user=user, nickname="관리자")


class Migration(migrations.Migration):

    dependencies = [
        (
            "user_profile",
            "0001_initial",
        ),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
