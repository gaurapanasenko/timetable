# Generated by Django 2.2.1 on 2019-05-09 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetableapp', '0034_auto_20190507_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='curriculumrecordteacher',
            name='subject',
            field=models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='timetableapp.CurriculumRecordSubject', verbose_name='subject'),
        ),
    ]
