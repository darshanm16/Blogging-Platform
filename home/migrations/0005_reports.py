# Generated by Django 5.1.3 on 2025-03-05 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_blogs_reported'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_id', models.ImageField(upload_to='')),
                ('user_id', models.IntegerField()),
            ],
        ),
    ]
