# Generated by Django 2.2 on 2019-04-29 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetableapp', '0035_auto_20190429_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='semesterschedule',
            name='startWeek',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Start week'),
        ),
    ]