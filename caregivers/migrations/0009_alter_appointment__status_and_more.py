# Generated by Django 4.2.5 on 2023-11-20 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caregivers', '0008_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='_status',
            field=models.CharField(choices=[('SCHEDULED', 'Scheduled'), ('PENDING', 'Pending')], max_length=50),
        ),
        migrations.AlterField(
            model_name='caregiver',
            name='caregiving_type',
            field=models.CharField(choices=[('BABYSITTER', 'Babysitter'), ('CAREGIVER_FOR_ELDERLY', 'Caregiver for elderly'), ('PLAYMATE_FOR_CHILDREN', 'Playmate for children')], max_length=50),
        ),
        migrations.AlterField(
            model_name='job',
            name='required_caregiving_type',
            field=models.CharField(choices=[('BABYSITTER', 'Babysitter'), ('CAREGIVER_FOR_ELDERLY', 'Caregiver for elderly'), ('PLAYMATE_FOR_CHILDREN', 'Playmate for children')], max_length=50),
        ),
    ]