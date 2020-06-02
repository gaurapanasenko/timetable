# Generated by Django 2.2.10 on 2020-06-02 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetableapp', '0002_auto_20200531_2235'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CurriculumRecordingTimings',
            new_name='CurriculumRecording',
        ),
        migrations.AlterModelOptions(
            name='building',
            options={'ordering': ['number'], 'verbose_name': 'building', 'verbose_name_plural': 'buildings'},
        ),
        migrations.AlterModelOptions(
            name='classroom',
            options={'ordering': ['building', 'number'], 'verbose_name': 'classroom', 'verbose_name_plural': 'classrooms'},
        ),
        migrations.AlterModelOptions(
            name='curriculum',
            options={'ordering': ('group_stream', 'semester'), 'verbose_name': 'curriculum', 'verbose_name_plural': 'curriculums'},
        ),
        migrations.AlterModelOptions(
            name='curriculumrecording',
            options={'ordering': ['group', 'semester'], 'verbose_name': 'curriculum record', 'verbose_name_plural': 'curriculum records'},
        ),
        migrations.AlterModelOptions(
            name='department',
            options={'ordering': ['abbreviation', 'name'], 'verbose_name': 'department', 'verbose_name_plural': 'departments'},
        ),
        migrations.AlterModelOptions(
            name='faculty',
            options={'ordering': ['abbreviation', 'name'], 'verbose_name': 'faculty', 'verbose_name_plural': 'faculties'},
        ),
        migrations.AlterModelOptions(
            name='formofstudy',
            options={'ordering': ['priority', 'suffix'], 'verbose_name': 'form of study', 'verbose_name_plural': 'forms of study'},
        ),
        migrations.AlterModelOptions(
            name='formofstudysemester',
            options={'verbose_name': 'semester date range', 'verbose_name_plural': 'semester date ranges'},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'group', 'verbose_name_plural': 'groups'},
        ),
        migrations.AlterModelOptions(
            name='groupstream',
            options={'ordering': ['-year', 'specialty', 'form'], 'verbose_name': 'group stream', 'verbose_name_plural': 'group streams'},
        ),
        migrations.AlterModelOptions(
            name='lesson',
            options={'verbose_name': 'lesson', 'verbose_name_plural': 'lessons'},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ['first_name', 'middle_name', 'last_name'], 'verbose_name': 'person', 'verbose_name_plural': 'persons'},
        ),
        migrations.AlterModelOptions(
            name='specialty',
            options={'ordering': ['abbreviation'], 'verbose_name': 'specialty', 'verbose_name_plural': 'specialties'},
        ),
        migrations.AlterModelOptions(
            name='subgroup',
            options={'verbose_name': 'subgroup', 'verbose_name_plural': 'subgroups'},
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={'ordering': ['name', 'department'], 'verbose_name': 'subject', 'verbose_name_plural': 'subjects'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'ordering': ['person'], 'verbose_name': 'teacher', 'verbose_name_plural': 'teachers'},
        ),
        migrations.AlterModelOptions(
            name='timetablerecording',
            options={'ordering': ['lesson__subgroup__denominator', 'lesson__subgroup__numerator'], 'verbose_name': 'timetable recording', 'verbose_name_plural': 'timetable recordings'},
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetableapp.Group', verbose_name='group'),
        ),
    ]
