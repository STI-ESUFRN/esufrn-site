# Generated by Django 4.0.9 on 2023-09-18 17:06

import core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Revista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_removed', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('LNK', 'Link'), ('DOC', 'Documento')], max_length=3, verbose_name='Tipo')),
                ('year', models.IntegerField(validators=[core.validators.year_validator], verbose_name='Ano')),
                ('subtitle', models.CharField(max_length=255, verbose_name='Subtítulo')),
                ('link', models.CharField(blank=True, max_length=255, null=True, verbose_name='Link')),
                ('file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='assets.file', verbose_name='Arquivo')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='assets.esimage', verbose_name='Capa da revista')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
