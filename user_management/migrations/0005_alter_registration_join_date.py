# Generated by Django 4.2 on 2025-02-15 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0004_alter_registration_join_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='join_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
