# Generated by Django 3.0.6 on 2020-06-17 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0006_auto_20200616_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default='Untitled', max_length=350),
        ),
    ]
