# Generated by Django 5.0.2 on 2024-03-18 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iadsapp', '0010_userprofile_bio_userprofile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='upcomingrelease',
            name='desc_game',
            field=models.TextField(default=''),
        ),
    ]