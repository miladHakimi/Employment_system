# Generated by Django 2.2.7 on 2019-11-13 21:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Accounting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default=django.utils.timezone.now, max_length=50, unique=True, verbose_name='user name'),
            preserve_default=False,
        ),
    ]
