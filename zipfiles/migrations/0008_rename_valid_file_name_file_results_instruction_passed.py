# Generated by Django 4.0.4 on 2023-07-05 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zipfiles', '0007_file_results_valid_file_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file_results',
            old_name='valid_file_name',
            new_name='instruction_passed',
        ),
    ]
