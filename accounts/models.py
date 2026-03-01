from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    avatar = CloudinaryField(
        'avatar',
        folder='starmediablog/authors/',
        blank=True,
        null=True
    )

    bio = models.TextField(blank=True)

    def str(self):
        return self.user.username