# Generated by Django 3.1.4 on 2020-12-30 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20201230_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schemas',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, verbose_name='last modified'),
        ),
    ]