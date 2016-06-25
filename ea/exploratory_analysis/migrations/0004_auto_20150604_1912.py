# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exploratory_analysis', '0003_variables'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packages',
            name='dataset_name',
            field=models.CharField(max_length=10000),
        ),
    ]
