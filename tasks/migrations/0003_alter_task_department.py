# Generated by Django 4.2.5 on 2023-10-04 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
        ('tasks', '0002_alter_task_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='employees.employee'),
        ),
    ]
