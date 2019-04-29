# Generated by Django 2.2 on 2019-04-29 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetableapp', '0031_auto_20190429_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curriculumentry',
            name='subject',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='timetableapp.Subject', verbose_name='Subject'),
        ),
        migrations.AlterField(
            model_name='curriculumentry',
            name='subjects',
            field=models.ManyToManyField(related_name='several_subjects', through='timetableapp.CurriculumEntrySubject', to='timetableapp.Subject', verbose_name='Subjects'),
        ),
    ]
