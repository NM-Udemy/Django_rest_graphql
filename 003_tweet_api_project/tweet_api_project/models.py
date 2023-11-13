from django.db import models
from django.contrib.auth import get_user_model

class Tweet(models.Model):
    text = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
