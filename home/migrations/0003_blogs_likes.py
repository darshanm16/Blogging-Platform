# Generated by Django 5.1.3 on 2025-01-17 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_blogs_ananymous'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogs',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
