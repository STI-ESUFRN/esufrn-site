# Generated by Django 4.0.9 on 2023-11-14 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chamado', '0004_alter_chamado_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='chamado',
            name='concorda',
            field=models.CharField(choices=[('y', 'SIM')], default=True, max_length=10, verbose_name='Marcando esta caixa você declara que estará presente no momento da manutenção'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chamado',
            name='date',
            field=models.DateField(null=True, verbose_name='Data *'),
        ),
        migrations.AddField(
            model_name='chamado',
            name='presenca',
            field=models.BooleanField(default=False, help_text='Marcando esta caixa, você declara que a sala contará com a supervisão de um docente no momento da aula.', verbose_name='Supervisionado por docente'),
        ),
        migrations.AddField(
            model_name='chamado',
            name='shift',
            field=models.CharField(choices=[('M', 'Manhã'), ('T', 'Tarde')], max_length=10, null=True, verbose_name='Turno *'),
        ),
        migrations.AlterField(
            model_name='chamado',
            name='contact',
            field=models.CharField(max_length=50, verbose_name='Whatsapp ou Email para contato'),
        ),
        migrations.AlterField(
            model_name='chamado',
            name='course',
            field=models.CharField(max_length=100, verbose_name='Nome do curso'),
        ),
        migrations.AlterField(
            model_name='chamado',
            name='description',
            field=models.TextField(max_length=300, verbose_name='Descrição do problema'),
        ),
        migrations.AlterField(
            model_name='chamado',
            name='requester',
            field=models.CharField(max_length=50, verbose_name='Nome completo'),
        ),
        migrations.AlterField(
            model_name='chamado',
            name='status',
            field=models.CharField(choices=[('R', 'Resolvido'), ('N', 'Não resolvido'), ('P', 'Pendente')], default='P', max_length=10, verbose_name='Status'),
        ),
    ]
