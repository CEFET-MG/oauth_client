# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth_client', '0003_oauthlogout'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OAuthLogout',
        ),
    ]
