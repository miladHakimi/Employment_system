# Generated by Django 2.2.7 on 2019-11-12 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Accounting', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applicant',
            old_name='Age',
            new_name='age',
        ),
        migrations.RenameField(
            model_name='employer',
            old_name='Address',
            new_name='address',
        ),
    ]
