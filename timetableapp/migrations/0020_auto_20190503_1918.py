# Generated by Django 2.2 on 2019-05-03 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetableapp', '0019_auto_20190503_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='group_stream',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='timetableapp.GroupStream', verbose_name='Group stream'),
        ),
    ]
