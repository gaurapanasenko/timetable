# Generated by Django 2.2 on 2019-05-03 10:42

from django.db import migrations
import yearlessdate.models


class Migration(migrations.Migration):

    dependencies = [
        ('timetableapp', '0013_auto_20190503_1003'),
    ]

    operations = [
        migrations.DeleteModel(
            name='formofstudysemester',
        ),
    ]