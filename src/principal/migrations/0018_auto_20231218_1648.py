# Generated by Django 3.2.8 on 2023-12-18 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0017_alter_cursos_pronatec_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='destaque',
            options={'verbose_name_plural': 'Destaque_PRONATEC'},
        ),
        migrations.AlterModelOptions(
            name='links_v',
            options={'verbose_name_plural': 'Videos_PRONATEC'},
        ),
    ]
