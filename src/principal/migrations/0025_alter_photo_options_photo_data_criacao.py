# Generated by Django 4.2.3 on 2024-06-24 17:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0024_auto_20240110_1505'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ['-data_criacao'], 'verbose_name_plural': 'Fotos_PRONATEC'},
        ),
        migrations.AddField(
            model_name='photo',
            name='data_criacao',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
