# Generated by Django 2.2.7 on 2019-11-13 10:45

import Accounting.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('userName', models.CharField(max_length=50, unique=True, verbose_name='user name')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('myuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Accounting.MyUser')),
                ('firstName', models.CharField(max_length=50, verbose_name='first name')),
                ('lastName', models.CharField(max_length=50, verbose_name='last name')),
                ('age', models.IntegerField(blank=True, default=18, verbose_name='Age')),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=20)),
                ('phone', models.CharField(blank=True, max_length=11, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('Accounting.myuser',),
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('myuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Accounting.MyUser')),
                ('companyName', models.CharField(max_length=50, verbose_name='company name')),
                ('establishedYear', models.DateTimeField(default=django.utils.timezone.now, verbose_name='established year')),
                ('address', models.CharField(blank=True, max_length=200, verbose_name='Address')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, validators=[Accounting.validators.PhoneValidator()])),
            ],
            options={
                'abstract': False,
            },
            bases=('Accounting.myuser',),
        ),
    ]
