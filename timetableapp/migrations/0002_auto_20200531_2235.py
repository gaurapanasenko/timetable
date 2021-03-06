# Generated by Django 2.2.1 on 2020-05-31 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetableapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='curriculum',
            options={'ordering': ('group_stream', 'semester'), 'verbose_name': 'Curriculum object', 'verbose_name_plural': 'curriculums'},
        ),
        migrations.AddField(
            model_name='lesson',
            name='teacher',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='timetableapp.Teacher', verbose_name='teacher'),
        ),
        migrations.AlterUniqueTogether(
            name='timetablerecording',
            unique_together={('lesson', 'lesson_number')},
        ),
        migrations.DeleteModel(
            name='LessonResponsible',
        ),
    ]
