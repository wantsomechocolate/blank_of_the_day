# Generated by Django 2.0 on 2019-03-23 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('useless_mutant', '0002_hashtag_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hashtag',
            name='test',
        ),
    ]