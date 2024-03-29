# Generated by Django 4.2 on 2023-05-02 16:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField(null=True)),
                ('sex', models.CharField(max_length=1)),
                ('height', models.DecimalField(decimal_places=2, max_digits=3)),
                ('starting_weight', models.DecimalField(decimal_places=2, max_digits=6)),
                ('aerobics', models.BooleanField(default=False)),
                ('recent_weight', models.DecimalField(decimal_places=2, default=models.DecimalField(decimal_places=2, max_digits=6), max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today, null=True)),
                ('new_weight', models.DecimalField(decimal_places=2, max_digits=6)),
                ('observations', models.CharField(max_length=200)),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.patient')),
            ],
        ),
    ]
