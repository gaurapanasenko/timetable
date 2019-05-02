# Generated by Django 2.2 on 2019-05-02 16:39

from django.db import migrations
import timetableapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('timetableapp', '0009_auto_20190502_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formofstudy',
            name='end_date_first',
            field=timetableapp.models.YearlessDateField(blank=True, default=None, null=True, verbose_name='End date for first semester'),
        ),
        migrations.AlterField(
            model_name='formofstudy',
            name='end_date_second',
            field=timetableapp.models.YearlessDateField(blank=True, default=None, null=True, verbose_name='End date for second semester'),
        ),
        migrations.AlterField(
            model_name='formofstudy',
            name='start_date_first',
            field=timetableapp.models.YearlessDateField(blank=True, default=None, null=True, verbose_name='Start date for first semester'),
        ),
        migrations.AlterField(
            model_name='formofstudy',
            name='start_date_second',
            field=timetableapp.models.YearlessDateField(blank=True, default=None, null=True, verbose_name='Start date for second semester'),
        ),
    ]
