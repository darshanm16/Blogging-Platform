# Generated by Django 5.1.3 on 2025-03-03 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogs',
            name='blockcomments',
            field=models.BooleanField(default=False),
        ),
    ]
