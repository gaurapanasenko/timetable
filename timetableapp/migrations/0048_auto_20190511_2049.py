# Generated by Django 2.2.1 on 2019-05-11 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetableapp', '0047_auto_20190511_2034'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='classroom',
            options={'ordering': ['building', 'number'], 'verbose_name': 'Classroom object', 'verbose_name_plural': 'classrooms'},
        ),
        migrations.AlterModelOptions(
            name='curriculum',
            options={'ordering': ['group', 'semester'], 'verbose_name': 'Curriculum object', 'verbose_name_plural': 'curriculums'},
        ),
        migrations.AlterModelOptions(
            name='formofstudy',
            options={'ordering': ['priority', 'suffix'], 'verbose_name': 'Form of study object', 'verbose_name_plural': 'forms of study'},
        ),
        migrations.AlterModelOptions(
            name='groupstream',
            options={'ordering': ['-year', 'specialty', 'form'], 'verbose_name': 'Group stream object', 'verbose_name_plural': 'group streams'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'ordering': ['person'], 'verbose_name': 'Teacher object', 'verbose_name_plural': 'teachers'},
        ),
    ]
