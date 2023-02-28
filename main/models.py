from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser) :
    friend_list = models.ManyToManyField("self", blank=True)

class Content(models.Model) :
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.CharField(max_length=1200)
    date = models.DateField()
    is_close_friend = models.BooleanField(default=False)


