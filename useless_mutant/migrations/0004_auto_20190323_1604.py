# Generated by Django 2.0 on 2019-03-23 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useless_mutant', '0003_remove_hashtag_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='hashtag',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='Hashtag',
        ),
    ]
