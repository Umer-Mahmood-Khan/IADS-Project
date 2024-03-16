# Generated by Django 5.0.2 on 2024-03-13 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iadsapp', '0006_award_game_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date', models.DateField()),
            ],
        ),
    ]