# Generated by Django 4.0.9 on 2023-10-04 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chamado', '0005_remove_chamado_presence_chamado_presenca'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamado',
            name='presenca',
            field=models.BooleanField(default=False, help_text='Marcando esta caixa, você declara que a sala contará com a supervisão de um docente no momento da aula.', verbose_name='Supervisionado por docente'),
        ),
    ]