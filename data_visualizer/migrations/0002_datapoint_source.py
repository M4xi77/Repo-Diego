# Generated by Django 3.2 on 2024-11-12 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_visualizer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='datapoint',
            name='source',
            field=models.CharField(default='manual', max_length=50),
        ),
    ]
