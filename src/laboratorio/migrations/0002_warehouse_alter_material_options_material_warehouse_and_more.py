# Generated by Django 4.0.9 on 2023-03-05 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('laboratorio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_removed', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Almoxarifado',
                'verbose_name_plural': 'Almoxarifados',
            },
        ),
        migrations.AlterModelOptions(
            name='material',
            options={'ordering': ['-name', '-created'], 'verbose_name': 'Material', 'verbose_name_plural': 'Materiais'},
        ),
        migrations.AddField(
            model_name='material',
            name='warehouse',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='materials', to='laboratorio.warehouse'),
        ),
        migrations.CreateModel(
            name='UserWarehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouses', to=settings.AUTH_USER_MODEL)),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsibles', to='laboratorio.warehouse')),
            ],
            options={
                'verbose_name': 'Responsável',
                'verbose_name_plural': 'Responsáveis',
                'unique_together': {('user', 'warehouse')},
            },
        ),
    ]