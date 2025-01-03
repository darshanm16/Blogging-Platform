# Generated by Django 5.1.3 on 2024-12-25 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_blogs_delete_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.CharField(max_length=100)),
                ('to_user', models.CharField(max_length=100)),
                ('blog_id', models.IntegerField()),
                ('comment', models.TextField(max_length=1000)),
            ],
        ),
    ]
