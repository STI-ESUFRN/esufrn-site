# Generated by Django 4.0.8 on 2023-02-10 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratorio', '0006_alter_consumable_managers_consumable_sold_out_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consumable',
            options={'ordering': ['-created'], 'verbose_name': 'Material de consumo', 'verbose_name_plural': 'Materiais de consumo'},
        ),
        migrations.RemoveField(
            model_name='consumable',
            name='reference',
        ),
        migrations.AddField(
            model_name='consumable',
            name='initial_quantity',
            field=models.IntegerField(blank=True, null=True, verbose_name='Quantidade inicial'),
        ),
    ]