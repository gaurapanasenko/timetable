# Generated by Django 2.2 on 2019-04-29 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetableapp', '0032_auto_20190429_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='curriculumentry',
            name='subject',
        ),
    ]