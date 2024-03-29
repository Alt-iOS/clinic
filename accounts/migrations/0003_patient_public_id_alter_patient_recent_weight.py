# Generated by Django 4.2 on 2023-05-03 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_appointment_new_weight_alter_patient_height_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='patient_id',
            field=models.CharField(default='1NV25Q2NAI', max_length=10),
        ),
        migrations.AlterField(
            model_name='patient',
            name='recent_weight',
            field=models.FloatField(max_length=6),
        ),
    ]
