# Generated by Django 4.2.5 on 2023-10-04 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_task_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='department',
            field=models.CharField(max_length=100),
        ),
    ]