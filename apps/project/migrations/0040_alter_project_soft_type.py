# Generated by Django 4.2.11 on 2024-06-11 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0039_round_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='soft_type',
            field=models.SmallIntegerField(choices=[(1, '新研'), (2, '改造'), (3, '沿用')], default=1, verbose_name='软件类型'),
        ),
    ]
