# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exploratory_analysis', '0002_delete_variables'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variables',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dataset_name', models.CharField(max_length=1000)),
                ('variables', models.TextField(null=True)),
            ],
        ),
    ]
