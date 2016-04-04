# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('installation', '0010_auto_20150907_1529'),
    ]

    operations = [
        migrations.CreateModel(
            name='MilitaryEquipment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0442\u0435\u0445\u043d\u0438\u043a\u0438')),
                ('picture', models.ImageField(null=True, upload_to=b'equipment', blank=True)),
                ('weight', models.FloatField(default=0, null=True, verbose_name='\u041c\u0430\u0441\u0441\u0430', blank=True)),
                ('length', models.FloatField(default=0, null=True, verbose_name='\u0414\u043b\u0438\u043d\u0430', blank=True)),
                ('width', models.FloatField(default=0, null=True, verbose_name='\u0428\u0438\u0440\u0438\u043d\u0430', blank=True)),
                ('height', models.FloatField(default=0, null=True, verbose_name='\u0412\u044b\u0441\u043e\u0442\u0430', blank=True)),
                ('truck_chassis', models.CharField(max_length=13, null=True, verbose_name='\u041a\u043e\u043b\u0451\u0441\u043d\u0430\u044f \u0444\u043e\u0440\u043c\u0443\u043b\u0430', blank=True)),
                ('accumulation_factor', models.CharField(max_length=13, null=True, verbose_name='\u041d\u043e\u0440\u043c\u0430 \u0440\u0430\u0437\u043c\u0435\u0449\u0435\u043d\u0438\u044f \u043f\u043b/\u043f\u0432', blank=True)),
            ],
            options={
                'verbose_name': '\u0412\u043e\u0435\u043d\u043d\u0430\u044f \u0442\u0435\u0445\u043d\u0438\u043a\u0430',
                'verbose_name_plural': '\u0412\u043e\u0435\u043d\u043d\u0430\u044f \u0442\u0435\u0445\u043d\u0438\u043a\u0430',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='icebreaker',
            name='building_place',
            field=models.CharField(max_length=100, null=True, verbose_name='\u041c\u0435\u0441\u0442\u043e \u043f\u043e\u0441\u0442\u0440\u043e\u0439\u043a\u0438', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='icebreaker',
            name='type_of_appy',
            field=models.CharField(max_length=100, null=True, verbose_name='\u0422\u0438\u043f \u0410\u041f\u041f\u0423', blank=True),
            preserve_default=True,
        ),
    ]
