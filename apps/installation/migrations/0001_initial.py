# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dist', models.FloatField(default=0, verbose_name='\u0420\u0430\u0441\u0441\u0442\u043e\u044f\u043d\u0438\u0435')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Port',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043f\u043e\u0440\u0442\u0430')),
                ('latitude', models.FloatField(default=0, verbose_name='\u0428\u0438\u0440\u043e\u0442\u0430')),
                ('longitude', models.FloatField(default=0, verbose_name='\u0414\u043e\u043b\u0433\u043e\u0442\u0430')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0432\u0430\u0437\u043d\u0438\u0435 \u0441\u0443\u0434\u043d\u0430')),
                ('speed_in_ballast', models.FloatField(default=0, verbose_name='\u0421\u043a\u043e\u0440\u043e\u0441\u0442\u044c \u0445\u043e\u0434\u0430 \u0432 \u0431\u0430\u043b\u043b\u0430\u0441\u0442\u0435')),
                ('speed_at_full_load', models.FloatField(default=0, verbose_name='\u0421\u043a\u043e\u0440\u043e\u0441\u0442\u044c \u0445\u043e\u0434\u0430 \u0432 \u043f\u043e\u043b\u043d\u043e\u043c \u0433\u0440\u0443\u0437\u0443')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='edge',
            name='from_port',
            field=models.ForeignKey(related_name='from_port', to='installation.Port'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='edge',
            name='to_port',
            field=models.ForeignKey(related_name='to_port', to='installation.Port'),
            preserve_default=True,
        ),
    ]
