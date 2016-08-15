from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    quote = models.CharField(max_length=140)

    def __unicode__(self):
        return self.user.username
