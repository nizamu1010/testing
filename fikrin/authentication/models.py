from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100, default='')
    profile_picture = models.ImageField(upload_to='profile_pictures/')
    bio = models.TextField(max_length=160, blank=True)
    cover_image1 = models.ImageField(upload_to='cover_images/')
    mobile_number = models.CharField(max_length=20)
    mobile_visible = models.BooleanField(default=True)


    def __str__(self):
        return self.user.username
