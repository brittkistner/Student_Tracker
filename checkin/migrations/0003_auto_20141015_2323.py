# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkin', '0002_remove_userprofile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='class_end',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='class',
            name='class_start',
            field=models.TimeField(),
        ),
    ]
