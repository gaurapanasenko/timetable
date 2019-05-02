# Generated by Django 2.2 on 2019-05-02 11:14

import django.core.validators
from django.db import migrations, models
import timetableapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('timetableapp', '0005_auto_20190502_1110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupstream',
            name='year',
            field=models.PositiveSmallIntegerField(default=timetableapp.models.current_year, validators=[django.core.validators.MinValueValidator(1900), timetableapp.models.year_max_value], verbose_name='Year'),
        ),
    ]
