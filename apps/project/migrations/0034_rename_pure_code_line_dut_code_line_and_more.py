# Generated by Django 4.2.11 on 2024-04-16 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0033_remove_dut_comment_line_remove_dut_total_code_line_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dut',
            old_name='pure_code_line',
            new_name='code_line',
        ),
        migrations.RenameField(
            model_name='dut',
            old_name='total_comment_line',
            new_name='comment_line',
        ),
    ]
