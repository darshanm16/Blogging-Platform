# Generated by Django 5.1.3 on 2025-02-23 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_details_delete_userdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='about',
            field=models.TextField(default='Add about you', max_length=1000),
        ),
        migrations.AlterField(
            model_name='details',
            name='dob',
            field=models.DateField(default='2000-01-01'),
        ),
        migrations.AlterField(
            model_name='details',
            name='role',
            field=models.CharField(default='Blogger', max_length=100),
        ),
        migrations.AlterField(
            model_name='details',
            name='saved',
            field=models.JSONField(default=list),
        ),
    ]
