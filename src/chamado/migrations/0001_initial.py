# Generated by Django 4.1 on 2022-09-01 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chamado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Título')),
                ('description', models.CharField(blank=True, max_length=300, null=True, verbose_name='Descrição')),
                ('requester', models.CharField(max_length=50, verbose_name='Solicitante')),
                ('course', models.CharField(max_length=100, verbose_name='Curso')),
                ('contact', models.CharField(blank=True, max_length=50, null=True, verbose_name='Whatsapp ou Email')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Registrado em')),
                ('solved_at', models.DateTimeField(blank=True, null=True, verbose_name='Resolvido em')),
                ('lastModified', models.DateTimeField(auto_now=True, verbose_name='Última modificação')),
                ('obs', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('status', models.BooleanField(null=True, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Chamado',
                'verbose_name_plural': 'Chamados',
                'ordering': ['-date'],
            },
        ),
    ]