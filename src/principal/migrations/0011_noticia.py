# Generated by Django 3.2.8 on 2023-12-04 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0010_alter_destaque_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('link', models.URLField()),
            ],
        ),
    ]
