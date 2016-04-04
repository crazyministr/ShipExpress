# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('installation', '0009_auto_20150907_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='icebreaker',
            name='picture',
            field=models.ImageField(null=True, upload_to=b'icebreakers', blank=True),
            preserve_default=True,
        ),
    ]
