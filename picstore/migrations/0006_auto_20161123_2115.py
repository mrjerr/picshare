# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 19:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('picstore', '0005_like'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='like',
            unique_together=set([('user', 'image')]),
        ),
    ]
