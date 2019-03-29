# Generated by Django 2.0 on 2019-03-23 07:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useless_mutant', '0004_auto_20190323_1604'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('name', models.CharField(max_length=100)),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.RenameField(
            model_name='post',
            old_name='hashtag',
            new_name='hashtag_name',
        ),
    ]
