# Generated by Django 2.2.7 on 2019-11-15 20:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounting', '0002_auto_20191116_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='establishedYear',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 16, 0, 27, 10, 295055), verbose_name='established year'),
        ),
    ]