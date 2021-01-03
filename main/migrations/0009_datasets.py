# Generated by Django 3.1.4 on 2021-01-02 13:45

from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20210101_1935'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataSets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('file', models.FileField(upload_to=main.models.user_directory_path)),
                ('ready', models.BooleanField(default=False)),
                ('schema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.schemas')),
            ],
        ),
    ]