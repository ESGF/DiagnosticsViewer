# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset_Access',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(max_length=1000)),
                ('dataset_list', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Packages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dataset_name', models.CharField(max_length=1000)),
                ('packages', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Published',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dataset_name', models.CharField(max_length=1000)),
                ('published', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Variables',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dataset_name', models.CharField(max_length=1000)),
                ('variables', models.TextField(null=True)),
            ],
        ),
    ]
