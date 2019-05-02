# Generated by Django 2.2 on 2019-05-01 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timetableapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialty',
            name='department',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='timetableapp.Department', verbose_name='Department'),
        ),
    ]