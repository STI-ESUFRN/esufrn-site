# Generated by Django 4.2.3 on 2024-07-08 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0026_alter_photo_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='ensino_subcategory',
            field=models.CharField(blank=True, choices=[('cursos_tecnicos', 'Cursos Técnicos'), ('graduacao_tecnologica', 'Graduação Tecnológica')], max_length=32, null=True, verbose_name='Subcategoria de Ensino'),
        ),
    ]
