# Generated by Django 3.2.8 on 2024-01-10 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0021_alter_noticia_titulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cursos_pronatec',
            name='nome_curso',
            field=models.CharField(max_length=400),
        ),
    ]