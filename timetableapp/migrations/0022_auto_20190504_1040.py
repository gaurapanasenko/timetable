# Generated by Django 2.2 on 2019-05-04 10:40

from django.db import migrations, models
import django.db.models.deletion
import yearlessdate.models


class Migration(migrations.Migration):

    dependencies = [
        ('timetableapp', '0021_auto_20190503_1922'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CurriculumEntry',
            new_name='CurriculumRecord',
        ),
        migrations.RenameModel(
            old_name='CurriculumEntrySubject',
            new_name='CurriculumRecordSubject',
        ),
        migrations.RenameModel(
            old_name='CurriculumEntryTeacher',
            new_name='CurriculumRecordTeacher',
        ),
    ]