# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth_client', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Pessoa',
        ),
    ]
