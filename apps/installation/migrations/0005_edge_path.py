# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('installation', '0004_auto_20150508_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='edge',
            name='path',
            field=jsonfield.fields.JSONField(default=[]),
            preserve_default=True,
        ),
    ]
