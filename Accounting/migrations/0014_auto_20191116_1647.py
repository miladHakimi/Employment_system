# Generated by Django 2.2.7 on 2019-11-16 13:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounting', '0013_auto_20191116_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='cv',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='employer',
            name='establishedYear',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 11, 16, 16, 47, 44, 538037), null=True, verbose_name='established year'),
        ),
    ]
