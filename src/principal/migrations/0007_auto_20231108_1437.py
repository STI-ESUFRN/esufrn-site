# Generated by Django 3.2.8 on 2023-11-08 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0006_destaque_video_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='destaque',
            name='tipo',
        ),
        migrations.RemoveField(
            model_name='destaque',
            name='video_url',
        ),
        migrations.AddField(
            model_name='destaque',
            name='titulo',
            field=models.CharField(default='Valor Padrão', max_length=25),
        ),
    ]
