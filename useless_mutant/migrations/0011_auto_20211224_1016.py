# Generated by Django 2.2.10 on 2021-12-24 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useless_mutant', '0010_auto_20190405_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='link',
            field=models.URLField(max_length=500),
        ),
    ]
