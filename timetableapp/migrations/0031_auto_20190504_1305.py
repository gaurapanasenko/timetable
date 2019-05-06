# Generated by Django 2.2 on 2019-05-04 13:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import timetableapp.models
import timetableapp.settings
import yearlessdate.models


class Migration(migrations.Migration):

    dependencies = [
        ('timetableapp', '0030_auto_20190504_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formofstudy',
            name='suffix',
            field=models.CharField(blank=True, max_length=16, unique=True, verbose_name='suffix'),
        ),
        migrations.AlterField(
            model_name='formofstudysemester',
            name='date_range',
            field=yearlessdate.models.YearlessDateRangeField(verbose_name='default date range'),
        ),
    ]