# Generated by Django 2.2 on 2019-04-28 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetableapp', '0018_auto_20190428_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='curriculumentry',
            name='subject',
            field=models.ManyToManyField(to='timetableapp.Subject', verbose_name='Subject'),
        ),
    ]
