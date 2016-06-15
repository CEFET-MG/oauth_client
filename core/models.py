from django.contrib.auth.models import User
from django.db import models

from django.db import models

class OAuthLogout(models.Model):
        access_token = models.CharField(max_length=255)

        class Meta:
                managed = True
