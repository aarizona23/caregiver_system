# Generated by Django 4.2.5 on 2023-11-20 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caregivers', '0009_alter_appointment__status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caregiver',
            name='gender',
            field=models.CharField(choices=[('FEMALE', 'Female'), ('MALE', 'Male')], max_length=50),
        ),
    ]