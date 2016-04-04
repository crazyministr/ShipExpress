# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('installation', '0003_auto_20150504_0050'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='edge',
            options={'verbose_name': '\u0420\u0430\u0441\u0441\u0442\u043e\u044f\u043d\u0438\u0435', 'verbose_name_plural': '\u0420\u0430\u0441\u0441\u0442\u043e\u044f\u043d\u0438\u044f'},
        ),
        migrations.AlterModelOptions(
            name='port',
            options={'verbose_name': '\u041f\u043e\u0440\u0442', 'verbose_name_plural': '\u041f\u043e\u0440\u0442\u044b'},
        ),
        migrations.AlterModelOptions(
            name='ship',
            options={'verbose_name': '\u0421\u0443\u0434\u043d\u043e', 'verbose_name_plural': '\u0421\u0443\u0434\u0430'},
        ),
        migrations.AddField(
            model_name='port',
            name='active',
            field=models.BooleanField(default=True, verbose_name='\u0410\u043a\u0442\u0438\u0432\u0435\u043d'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ship',
            name='active',
            field=models.BooleanField(default=True, verbose_name='\u0410\u043a\u0442\u0438\u0432\u0435\u043d'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='port',
            name='airport',
            field=models.CharField(default=b'', max_length=100, verbose_name='\u0410\u044d\u0440\u043e\u043f\u043e\u0440\u0442', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='port',
            name='ice_period',
            field=models.CharField(default=b'', max_length=100, verbose_name='\u041b\u0435\u0434\u043e\u0432\u044b\u0439 \u043f\u0435\u0440\u0438\u043e\u0434', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='port',
            name='location',
            field=models.CharField(default=b'', max_length=100, verbose_name='\u041c\u0435\u0441\u0442\u043e\u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u0435', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='port',
            name='navigation',
            field=models.CharField(default=b'', max_length=100, verbose_name='\u041d\u0430\u0432\u0438\u0433\u0430\u0446\u0438\u044f', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='port',
            name='oil_terminals',
            field=models.CharField(default=b'', max_length=100, verbose_name='\u041d\u0430\u043b\u0438\u0447\u0438\u0435 \u043d\u0435\u0444\u0442\u0435\u043d\u0430\u043b\u0438\u0432\u043d\u044b\u0445 \u0442\u0435\u0440\u043c\u0438\u043d\u0430\u043b\u043e\u0432', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='port',
            name='railway',
            field=models.CharField(default=b'', max_length=100, verbose_name='\u0416\u0435\u043b\u0435\u0437\u043d\u0430\u044f \u0434\u043e\u0440\u043e\u0433\u0430', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='port',
            name='surrounding_towns',
            field=models.CharField(default=b'', max_length=100, verbose_name='\u0411\u043b\u0438\u0436\u0430\u0439\u0448\u0438\u0435 \u043d\u0430\u0441\u0435\u043b\u0435\u043d\u043d\u044b\u0435 \u043f\u0443\u043d\u043a\u0442\u044b', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ship',
            name='picture',
            field=models.ImageField(null=True, upload_to=b'ships', blank=True),
            preserve_default=True,
        ),
    ]
