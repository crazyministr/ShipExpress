# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.installation.models


class Migration(migrations.Migration):

    dependencies = [
        ('installation', '0008_auto_20150624_0143'),
    ]

    operations = [
        migrations.CreateModel(
            name='Icebreaker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0432\u0430\u0437\u043d\u0438\u0435 \u0441\u0443\u0434\u043d\u0430')),
                ('picture', models.ImageField(null=True, upload_to=b'ships', blank=True)),
                ('building_place', models.CharField(max_length=100, verbose_name='\u041c\u0435\u0441\u0442\u043e \u043f\u043e\u0441\u0442\u0440\u043e\u0439\u043a\u0438')),
                ('length_max', models.FloatField(default=0, null=True, verbose_name='\u0414\u043b\u0438\u043d\u0430 \u043d\u0430\u0438\u0431\u043e\u043b\u044c\u0448\u0430\u044f, \u043c.', blank=True)),
                ('width_max', models.FloatField(default=0, null=True, verbose_name='\u0428\u0438\u0440\u0438\u043d\u0430 \u043d\u0430\u0438\u0431\u043e\u043b\u044c\u0448\u0430\u044f, \u043c.', blank=True)),
                ('displacement', models.FloatField(default=0, null=True, verbose_name='\u0412\u043e\u0434\u043e\u0438\u0437\u043c\u0435\u0449\u0435\u043d\u0438\u0435, \u0442.', blank=True)),
                ('propulsion_power', models.FloatField(default=0, null=True, verbose_name='\u041f\u0440\u043e\u043f\u0443\u043b\u044c\u0441\u0438\u0432\u043d\u0430\u044f \u043c\u043e\u0449\u043d\u043e\u0441\u0442\u044c, \u041c\u0412\u0442', blank=True)),
                ('type_of_appy', models.CharField(max_length=100, verbose_name='\u0422\u0438\u043f \u0410\u041f\u041f\u0423')),
                ('speed', models.FloatField(default=0, null=True, verbose_name='\u0421\u043a\u043e\u0440\u043e\u0441\u0442\u044c \u0445\u043e\u0434\u0430, \u0443\u0437\u043b.', blank=True)),
                ('endurance', models.FloatField(default=0, null=True, verbose_name='\u0410\u0432\u0442\u043e\u043d\u043e\u043c\u043d\u043e\u0441\u0442\u044c \u043f\u043b\u0430\u0432\u0430\u043d\u0438\u044f, \u043c\u0435\u0441.', blank=True)),
                ('ice_passability', models.FloatField(default=0, null=True, verbose_name='\u041b\u0435\u0434\u043e\u043f\u0440\u043e\u0445\u043e\u0434\u0438\u043c\u043e\u0441\u0442\u044c, \u043c.', blank=True)),
            ],
            options={
                'verbose_name': '\u041b\u0435\u0434\u043e\u043a\u043e\u043b',
                'verbose_name_plural': '\u041b\u0435\u0434\u043e\u043a\u043e\u043b\u044b',
            },
            bases=(models.Model, apps.installation.models.UrlGen),
        ),
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
    ]
