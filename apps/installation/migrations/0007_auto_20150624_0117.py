# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('installation', '0006_auto_20150623_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ship',
            name='ammunition',
            field=models.IntegerField(default=0, null=True, verbose_name='\u0411\u043e\u0435\u043f\u0440\u0438\u043f\u0430\u0441\u044b, \u0442.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ship',
            name='armoured',
            field=models.IntegerField(default=0, null=True, verbose_name='\u0411\u0440\u043e\u043d\u0435\u0442\u0440\u0430\u043d\u0441\u043f\u043e\u0440\u0442\u0451\u0440\u044b, \u0435\u0434.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ship',
            name='artillery',
            field=models.IntegerField(default=0, null=True, verbose_name='\u0410\u0440\u0442\u0438\u043b\u043b\u0435\u0440\u0438\u044f, \u0435\u0434.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ship',
            name='cars',
            field=models.IntegerField(default=0, null=True, verbose_name='\u0410\u0432\u0442\u043e\u043c\u043e\u0431\u0438\u043b\u0438, \u0435\u0434.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ship',
            name='clothing_equipment',
            field=models.IntegerField(default=0, null=True, verbose_name='\u0412\u0435\u0449\u0435\u0432\u043e\u0435 \u0438\u043c\u0443\u0449\u0435\u0441\u0442\u0432\u043e, \u0442.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ship',
            name='displacement',
            field=models.FloatField(default=0, null=True, verbose_name='\u0412\u043e\u0434\u043e\u0438\u0437\u043c\u0435\u0449\u0435\u043d\u0438\u0435, \u0442.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ship',
            name='draft_at_full_load',
            field=models.FloatField(default=0, null=True, verbose_name='\u041e\u0441\u0430\u0434\u043a\u0430 \u0432 \u043f\u043e\u043b\u043d\u043e\u043c \u0433\u0440\u0443\u0437\u0443, \u043c.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ship',
            name='draft_ballast',
            field=models.FloatField(default=0, null=True, verbose_name='\u041e\u0441\u0430\u0434\u043a\u0430 \u0432 \u0431\u0430\u043b\u043b\u0430\u0441\u0442\u0435, \u043c.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ship',
            name='food',
            field=models.IntegerField(default=0, null=True, verbose_name='\u041f\u0440\u043e\u0434\u043e\u0432\u043e\u043b\u044c\u0441\u0442\u0432\u0438\u0435, \u0442.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ship',
            name='fuel_in_containers',
            field=models.IntegerField(default=0, null=True, verbose_name='\u0413\u043e\u0440\u044e\u0447\u0435\u0435 \u0432 \u0442\u0430\u0440\u0435, \u0442.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ship',
            name='length_max',
            field=models.FloatField(default=0, null=True, verbose_name='\u0414\u043b\u0438\u043d\u0430 \u043d\u0430\u0438\u0431\u043e\u043b\u044c\u0448\u0430\u044f, \u043c.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ship',
            name='living_space_decks',
            field=models.FloatField(default=0, null=True, verbose_name='\u041f\u043e\u043b\u0435\u0437\u043d\u0430\u044f \u043f\u043b\u043e\u0449\u0430\u0434\u044c \u043f\u0430\u043b\u0443\u0431, \u043a\u0432. \u043c.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ship',
            name='load_capacity',
            field=models.FloatField(default=0, null=True, verbose_name='\u0413\u0440\u0443\u0437\u043e\u043f\u043e\u0434\u044a\u0451\u043c\u043d\u043e\u0441\u0442\u044c \u0447\u0438\u0441\u0442\u0430\u044f, \u0442.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ship',
            name='speed_at_full_load',
            field=models.FloatField(default=0, null=True, verbose_name='\u0421\u043a\u043e\u0440\u043e\u0441\u0442\u044c \u0445\u043e\u0434\u0430 \u0432 \u043f\u043e\u043b\u043d\u043e\u043c \u0433\u0440\u0443\u0437\u0443, \u0443\u0437\u043b.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ship',
            name='speed_in_ballast',
            field=models.FloatField(default=0, null=True, verbose_name='\u0421\u043a\u043e\u0440\u043e\u0441\u0442\u044c \u0445\u043e\u0434\u0430 \u0432 \u0431\u0430\u043b\u043b\u0430\u0441\u0442\u0435, \u0443\u0437\u043b.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ship',
            name='staff',
            field=models.IntegerField(default=0, null=True, verbose_name='\u041b\u0438\u0447\u043d\u044b\u0439 \u0441\u043e\u0441\u0442\u0430\u0432, \u0447\u0435\u043b.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ship',
            name='tanks',
            field=models.IntegerField(default=0, null=True, verbose_name='\u0422\u0430\u043d\u043a\u0438, \u0435\u0434.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ship',
            name='width_max',
            field=models.FloatField(default=0, null=True, verbose_name='\u0428\u0438\u0440\u0438\u043d\u0430 \u043d\u0430\u0438\u0431\u043e\u043b\u044c\u0448\u0430\u044f, \u043c.', blank=True),
            preserve_default=True,
        ),
    ]
