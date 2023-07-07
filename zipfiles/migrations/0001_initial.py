# Generated by Django 4.0.4 on 2023-07-07 12:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserNamesList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=255, unique=True, validators=[django.core.validators.MinLengthValidator(3, message='Username must have at least 3 characters.')])),
                ('email', models.EmailField(max_length=254)),
                ('enable', models.BooleanField(default=True)),
                ('updated_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'UserNamesList',
            },
        ),
        migrations.CreateModel(
            name='File_Results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_number', models.PositiveIntegerField(null=True)),
                ('f_name', models.CharField(max_length=255, null=True)),
                ('f_size', models.CharField(max_length=50, null=True)),
                ('myfiles', models.FileField(upload_to='')),
                ('db_name', models.CharField(max_length=50, null=True)),
                ('db_type', models.CharField(max_length=50, null=True)),
                ('is_build_succeeded', models.CharField(max_length=50, null=True)),
                ('dotnet_version', models.CharField(max_length=20, null=True)),
                ('assignment_number', models.IntegerField(null=True)),
                ('folder_name', models.CharField(max_length=50, null=True)),
                ('instruction_passed', models.CharField(max_length=50, null=True)),
                ('user_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='zipfiles.usernameslist')),
            ],
        ),
    ]
