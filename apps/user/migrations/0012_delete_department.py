# Generated by Django 4.2.11 on 2024-06-03 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_remove_department_parent_department_parent'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Department',
        ),
    ]
