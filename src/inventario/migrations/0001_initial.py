# Generated by Django 4.1 on 2022-09-01 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reserva', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emprestimo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Solicitante')),
                ('contact', models.CharField(max_length=100, null=True, verbose_name='Contato')),
                ('obs', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Contato')),
                ('borrow_date', models.DateTimeField(verbose_name='Data de empréstimo')),
                ('return_date', models.DateTimeField(blank=True, null=True, verbose_name='Recebido em')),
                ('status', models.CharField(choices=[('A', 'Aguardando devolução'), ('D', 'Devolvido'), ('C', 'Cancelado')], default='A', max_length=1)),
                ('classroom', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reserva.classroom', verbose_name='Sala')),
            ],
        ),
        migrations.CreateModel(
            name='Patrimonio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=64, verbose_name='Modelo')),
                ('dmp', models.CharField(blank=True, max_length=64, null=True, verbose_name='Tombamento')),
                ('category', models.CharField(choices=[('C', 'Computador de mesa'), ('N', 'Notebook'), ('D', 'Projetor'), ('P', 'Periférico'), ('E', 'Cabo'), ('O', 'Outro')], max_length=1, verbose_name='Tipo')),
                ('status', models.CharField(choices=[('D', 'Disponível'), ('E', 'Emprestado')], default='D', max_length=1, verbose_name='Status')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='Última atualização')),
            ],
        ),
        migrations.CreateModel(
            name='PatrimonioEmprestimo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='Quantidade')),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.emprestimo')),
                ('patrimony', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.patrimonio')),
            ],
            options={
                'verbose_name': 'Equipamento',
                'verbose_name_plural': 'Equipamentos',
                'ordering': ['patrimony__model'],
            },
        ),
        migrations.CreateModel(
            name='Maquina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ram', models.IntegerField(blank=True, null=True, verbose_name='RAM')),
                ('hdd', models.IntegerField(blank=True, null=True, verbose_name='HDD')),
                ('status', models.CharField(choices=[('R', 'Reserva'), ('G', 'Bom'), ('W', 'Atenção'), ('B', 'Ruim')], max_length=1, verbose_name='Status')),
                ('obs', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Observações')),
                ('patrimony', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.patrimonio', verbose_name='Patrimônio')),
            ],
            options={
                'verbose_name': 'Máquina',
                'verbose_name_plural': 'Máquinas',
                'ordering': ['patrimony__model', 'patrimony__dmp'],
            },
        ),
    ]