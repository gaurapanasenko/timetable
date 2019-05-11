# Generated by Django 2.2.1 on 2019-05-11 20:23

from django.db import migrations, models
import timetableapp.models
import timetableapp.settings


class Migration(migrations.Migration):

    dependencies = [
        ('timetableapp', '0044_auto_20190511_2011'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='curriculum',
            options={'ordering': ['group__group_stream__year', 'group__number'], 'verbose_name': 'Curriculum object', 'verbose_name_plural': 'curriculums'},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'Group object', 'verbose_name_plural': 'groups'},
        ),
        migrations.AlterField(
            model_name='group',
            name='number',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(None, '-'), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)], db_index=True, default=None, null=True, verbose_name='number'),
        ),
        migrations.AlterField(
            model_name='groupstream',
            name='year',
            field=models.PositiveSmallIntegerField(db_index=True, default=timetableapp.settings.current_year, validators=[timetableapp.models.year_min_value, timetableapp.models.year_max_value], verbose_name='year'),
        ),
        migrations.AlterIndexTogether(
            name='group',
            index_together={('parent', 'group_stream', 'number')},
        ),
    ]
