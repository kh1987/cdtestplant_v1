# Generated by Django 4.2.3 on 2023-08-17 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_alter_project_plant_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='dev_ident',
        ),
        migrations.RemoveField(
            model_name='project',
            name='dev_legal',
        ),
        migrations.RemoveField(
            model_name='project',
            name='entrust_ident',
        ),
        migrations.RemoveField(
            model_name='project',
            name='entrust_legal',
        ),
        migrations.RemoveField(
            model_name='project',
            name='test_ident',
        ),
        migrations.RemoveField(
            model_name='project',
            name='test_legal',
        ),
    ]
