# Generated by Django 4.2.7 on 2024-02-22 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Base', '0003_rename_file_picklefile_train_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='file',
        ),
        migrations.RemoveField(
            model_name='picklefile',
            name='Train_file',
        ),
        migrations.AddField(
            model_name='file',
            name='Train_file',
            field=models.FileField(blank=True, null=True, upload_to='testfiles'),
        ),
        migrations.AddField(
            model_name='picklefile',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='pickle_files/'),
        ),
    ]