# Generated by Django 4.0.4 on 2023-06-09 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zipfiles', '0003_rename_gpa_zipfile_dotnet_version'),
    ]

    operations = [
        migrations.CreateModel(
            name='myuploadfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(max_length=255)),
                ('myfiles', models.FileField(upload_to='')),
            ],
        ),
    ]