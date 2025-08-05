from django.db import models


def user_directory_path(instance, filename):
    return f"avatars/{instance.user.id}/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="account",
        verbose_name="User",
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Birth Date",
    )
    avatar = models.ImageField(
        upload_to=user_directory_path,
        blank=True,
        null=True,
        verbose_name="Avatar",
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name="Bio",
    )
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Account"
