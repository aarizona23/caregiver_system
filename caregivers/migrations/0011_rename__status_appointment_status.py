# Generated by Django 4.2.5 on 2023-11-20 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('caregivers', '0010_alter_caregiver_gender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='_status',
            new_name='status',
        ),
    ]