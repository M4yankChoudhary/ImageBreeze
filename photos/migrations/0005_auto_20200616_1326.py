# Generated by Django 3.0.6 on 2020-06-16 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0004_auto_20200616_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercomment',
            name='time',
            field=models.CharField(max_length=10),
        ),
    ]