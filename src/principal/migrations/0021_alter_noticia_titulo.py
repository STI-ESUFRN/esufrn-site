# Generated by Django 3.2.8 on 2024-01-10 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0020_alter_noticia_titulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticia',
            name='titulo',
            field=models.CharField(max_length=100),
        ),
    ]