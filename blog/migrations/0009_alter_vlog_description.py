# Generated by Django 5.0.7 on 2024-12-23 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_likevlog_unique_together_remove_likevlog_vlog_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vlog',
            name='description',
            field=models.CharField(max_length=50),
        ),
    ]
