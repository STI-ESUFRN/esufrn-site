# Generated by Django 4.0.9 on 2023-09-18 17:04

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ESImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('high', models.ImageField(upload_to='images', verbose_name='Imagem (qualidade original)')),
                ('medium', models.ImageField(blank=True, null=True, upload_to='images', verbose_name='Imagem (qualidade média)')),
                ('low', models.ImageField(blank=True, null=True, upload_to='images', verbose_name='Imagem (qualidade baixa)')),
            ],
            options={
                'verbose_name': 'Imagem',
                'verbose_name_plural': 'Imagens',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('url', models.FileField(upload_to='files')),
            ],
            options={
                'verbose_name': 'Arquivo',
                'verbose_name_plural': 'Arquivos',
                'ordering': ['-created'],
            },
        ),
    ]
