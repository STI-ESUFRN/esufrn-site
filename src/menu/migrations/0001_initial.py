# Generated by Django 4.1 on 2022-09-01 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Itens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('action_type', models.CharField(choices=[('hover', 'Hover'), ('link', 'Link')], default='hover', help_text='Hover: Ao clicar ou passar o mouse sobre, abrirá os subitens; Link: Ao clicar abrirá o link inserido.', max_length=100, verbose_name='Tipo')),
                ('footer', models.BooleanField(default=False, help_text='Mostrar menu e seus respectivos subitens no rodapé da página', verbose_name='Rodapé')),
                ('link', models.CharField(blank=True, help_text='Usar apenas se o tipo for Link', max_length=255, verbose_name='Link')),
                ('order', models.IntegerField(help_text='Ordem que aparecerá na barra de menu', verbose_name='Ordem')),
                ('decoration', models.CharField(blank=True, help_text='Classes CSS extra', max_length=100, null=True, verbose_name='Class estilo')),
            ],
            options={
                'verbose_name': 'Menu nível 1',
                'verbose_name_plural': 'Menu nível 1',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='SubItens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('action_type', models.CharField(choices=[('hover', 'Hover'), ('link', 'Link')], default='hover', help_text='Hover: Ao clicar ou passar o mouse sobre, abrirá os subitens; Link: Ao clicar abrirá o link inserido.', max_length=100, verbose_name='Tipo')),
                ('link', models.CharField(max_length=255, verbose_name='Link')),
                ('order', models.IntegerField(verbose_name='Ordem')),
                ('decoration', models.CharField(blank=True, help_text='Classes CSS extra', max_length=100, null=True, verbose_name='Class estilo')),
                ('menu', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.itens')),
            ],
            options={
                'verbose_name': 'Menu nível 2',
                'verbose_name_plural': 'Menu nível 2',
                'ordering': ['menu', 'order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='SubSubItens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('link', models.CharField(max_length=255, verbose_name='Link')),
                ('order', models.IntegerField(verbose_name='Ordem')),
                ('decoration', models.CharField(blank=True, help_text='Classes CSS extra', max_length=100, null=True, verbose_name='Class estilo')),
                ('submenu', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.subitens')),
            ],
            options={
                'verbose_name': 'Menu nível 3',
                'verbose_name_plural': 'Menu nível 3',
                'ordering': ['submenu', 'order', 'name'],
            },
        ),
    ]