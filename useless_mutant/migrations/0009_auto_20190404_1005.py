# Generated by Django 2.1.7 on 2019-04-04 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useless_mutant', '0008_hashtag_last_post_added_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='search_query',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='post',
            name='search_query_raw',
            field=models.TextField(max_length=500),
        ),
    ]
