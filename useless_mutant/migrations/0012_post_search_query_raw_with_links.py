# Generated by Django 2.2.10 on 2021-12-25 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useless_mutant', '0011_auto_20211224_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='search_query_raw_with_links',
            field=models.TextField(default='The original tweet data is not available for this post', max_length=500),
            preserve_default=False,
        ),
    ]
