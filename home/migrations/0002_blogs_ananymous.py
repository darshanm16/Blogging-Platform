# Generated by Django 5.1.3 on 2025-01-15 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogs',
            name='ananymous',
            field=models.BooleanField(default=False),
        ),
    ]