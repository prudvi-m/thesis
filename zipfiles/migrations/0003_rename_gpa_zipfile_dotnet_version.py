# Generated by Django 4.0.4 on 2023-06-09 04:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zipfiles', '0002_rename_field_of_study_zipfile_db_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='zipfile',
            old_name='gpa',
            new_name='dotnet_version',
        ),
    ]