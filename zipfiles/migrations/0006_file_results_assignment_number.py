# Generated by Django 4.0.4 on 2023-07-04 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zipfiles', '0005_alter_file_results_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='file_results',
            name='assignment_number',
            field=models.IntegerField(null=True),
        ),
    ]