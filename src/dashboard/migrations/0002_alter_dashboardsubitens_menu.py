# Generated by Django 4.0.8 on 2022-11-30 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardsubitens',
            name='menu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subitems', to='dashboard.dashboarditens'),
        ),
    ]