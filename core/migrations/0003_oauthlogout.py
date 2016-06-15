# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_delete_pessoa'),
    ]

    operations = [
        migrations.CreateModel(
            name='OAuthLogout',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('access_token', models.CharField(max_length=255)),
            ],
            options={
                'managed': True,
            },
        ),
    ]
