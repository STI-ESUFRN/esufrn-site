# Generated by Django 4.0.9 on 2023-03-21 01:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_alter_dashboardsubitens_menu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dashboardsubitens',
            name='related_name',
        ),
    ]