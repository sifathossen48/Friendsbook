# Generated by Django 4.2 on 2025-02-15 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0006_rename_join_date_registration_join'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registration',
            old_name='join',
            new_name='just_join',
        ),
    ]
