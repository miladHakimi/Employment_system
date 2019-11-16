# Generated by Django 2.2.7 on 2019-11-15 20:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Accounting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('profile_img', models.ImageField(blank=True, upload_to='')),
                ('expDate', models.DateField(blank=True, default=datetime.date.today)),
                ('fieldsOfExpertise', models.CharField(choices=[('programming', 'Programmer'), ('mechanical_engineering', 'Mechanical Engineer')], max_length=20)),
                ('salary', models.CharField(max_length=10)),
                ('employer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ads', to='Accounting.Employer')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.BooleanField(default=False, null=True)),
                ('rejected', models.BooleanField(default=False, null=True)),
                ('ad', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ad', to='Commercial.Ad')),
                ('applicant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='request', to='Accounting.Applicant')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(null=True)),
                ('applicant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aplicant', to='Accounting.Applicant')),
                ('employer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employer', to='Accounting.Employer')),
            ],
        ),
    ]