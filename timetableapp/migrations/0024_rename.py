# Generated by Django 2.2 on 2019-05-04 10:40

from django.db import migrations, models
import django.db.models.deletion
import yearlessdate.models


class Migration(migrations.Migration):

    dependencies = [
        ('timetableapp', '0023_auto_20190504_1043'),
    ]

    operations = [
        migrations.RenameField(
            model_name='curriculumrecordsubject',
            old_name='entry',
            new_name='record',
        ),
    ]
