# Generated by Django 4.2.3 on 2024-06-24 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0025_alter_photo_options_photo_data_criacao'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ['-date_created'], 'verbose_name_plural': 'Fotos_PRONATEC'},
        ),
        migrations.RenameField(
            model_name='photo',
            old_name='data_criacao',
            new_name='date_created',
        ),
    ]
