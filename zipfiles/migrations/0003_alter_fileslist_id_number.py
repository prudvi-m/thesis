# Generated by Django 4.0.4 on 2023-06-09 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zipfiles', '0002_fileslist_myuploadfile_delete_zipfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileslist',
            name='id_number',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
