# Generated by Django 3.0.6 on 2020-06-16 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0002_auto_20200616_1318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercomment',
            name='date',
        ),
        migrations.RemoveField(
            model_name='usercomment',
            name='time',
        ),
        migrations.RemoveField(
            model_name='usercomment',
            name='username',
        ),
    ]
