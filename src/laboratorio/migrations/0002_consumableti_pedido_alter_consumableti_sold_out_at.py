from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratorio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumableti',
            name='pedido',
            field=models.CharField(choices=[('Solicitado', 'Solicitado'), ('Não solicitado', 'Não solicitado')], default='Não solicitado', max_length=15),
        ),
        migrations.AlterField(
            model_name='consumableti',
            name='sold_out_at',
            field=models.DateField(blank=True, null=True, verbose_name='Pedido em'),
        ),
    ]
