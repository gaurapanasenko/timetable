# Generated by Django 2.2.1 on 2019-05-07 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetableapp', '0033_auto_20190504_1310'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='building',
            options={'verbose_name': 'Building object', 'verbose_name_plural': 'buildings'},
        ),
        migrations.AlterModelOptions(
            name='classroom',
            options={'verbose_name': 'Classroom object', 'verbose_name_plural': 'classrooms'},
        ),
        migrations.AlterModelOptions(
            name='curriculum',
            options={'verbose_name': 'Curriculum object', 'verbose_name_plural': 'curriculums'},
        ),
        migrations.AlterModelOptions(
            name='curriculumrecord',
            options={'verbose_name': 'Curriculum record object', 'verbose_name_plural': 'curriculum records'},
        ),
        migrations.AlterModelOptions(
            name='curriculumrecordsubject',
            options={'verbose_name': 'Subject for curriculum record object', 'verbose_name_plural': 'subjects for curriculum records'},
        ),
        migrations.AlterModelOptions(
            name='curriculumrecordteacher',
            options={'verbose_name': 'Teacher for curriculum record object', 'verbose_name_plural': 'teachers for curriculum records'},
        ),
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name': 'Department object', 'verbose_name_plural': 'departments'},
        ),
        migrations.AlterModelOptions(
            name='faculty',
            options={'verbose_name': 'Faculty object', 'verbose_name_plural': 'faculties'},
        ),
        migrations.AlterModelOptions(
            name='formofstudy',
            options={'ordering': ['priority'], 'verbose_name': 'Form of study object', 'verbose_name_plural': 'forms of study'},
        ),
        migrations.AlterModelOptions(
            name='formofstudysemester',
            options={'verbose_name': 'Semester date range object', 'verbose_name_plural': 'semester date ranges'},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'Group object', 'verbose_name_plural': 'groups'},
        ),
        migrations.AlterModelOptions(
            name='groupstream',
            options={'verbose_name': 'Group stream object', 'verbose_name_plural': 'group streams'},
        ),
        migrations.AlterModelOptions(
            name='groupstreamsemester',
            options={'verbose_name': 'Group stream semester object', 'verbose_name_plural': 'group stream semesters'},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'Person object', 'verbose_name_plural': 'persons'},
        ),
        migrations.AlterModelOptions(
            name='specialty',
            options={'verbose_name': 'Specialty object', 'verbose_name_plural': 'specialties'},
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={'verbose_name': 'Subject object', 'verbose_name_plural': 'subjects'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'verbose_name': 'Teacher object', 'verbose_name_plural': 'teachers'},
        ),
        migrations.AlterModelOptions(
            name='timetablerecording',
            options={'verbose_name': 'Timetable recording object', 'verbose_name_plural': 'timetable recordings'},
        ),
        migrations.AlterIndexTogether(
            name='group',
            index_together={('parent', 'group_stream')},
        ),
    ]