# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True, editable=False, default=uuid.uuid4)),
                ('firstname', models.CharField(verbose_name='First Name', max_length=55)),
                ('lastname', models.CharField(verbose_name='Last Name', max_length=55)),
                ('date_of_birth', models.DateField(verbose_name='Date of Birth')),
                ('zip_code', models.CharField(verbose_name='Zip Code', max_length=55)),
            ],
        ),
    ]
