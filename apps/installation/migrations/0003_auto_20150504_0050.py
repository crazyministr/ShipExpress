# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('installation', '0002_auto_20150429_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='port',
            name='picture',
            field=models.ImageField(null=True, upload_to=b'ports', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ship',
            name='picture',
            field=models.ImageField(null=True, upload_to=b'ports', blank=True),
            preserve_default=True,
        ),
    ]
