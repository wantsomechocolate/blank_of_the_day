# Generated by Django 2.0 on 2019-03-23 06:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('search_query', models.CharField(max_length=100)),
                ('link', models.URLField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('votes', models.IntegerField(default=0)),
                ('current_streak', models.IntegerField(default=0)),
                ('max_streak', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('hashtag', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='useless_mutant.Hashtag')),
            ],
        ),
    ]