# Generated by Django 4.0.8 on 2022-12-08 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserva', '0007_alter_reserve_shift'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='event',
            field=models.CharField(max_length=100, verbose_name='Evento'),
        ),
    ]