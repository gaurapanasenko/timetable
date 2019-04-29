# Generated by Django 2.2 on 2019-04-29 10:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetableapp', '0027_auto_20190429_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='workTime',
            field=models.BigIntegerField(default=1152921504606846976, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1152921504606846976)], verbose_name='Work time'),
        ),
    ]
