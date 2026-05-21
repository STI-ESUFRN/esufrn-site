from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chamado", "0005_chamado_concorda_chamado_date_chamado_presenca_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="chamado",
            old_name="title",
            new_name="equipment",
        ),
        migrations.RenameField(
            model_name="chamado",
            old_name="course",
            new_name="room",
        ),
        migrations.RenameField(
            model_name="chamado",
            old_name="contact",
            new_name="tombamento",
        ),
        migrations.RemoveField(
            model_name="chamado",
            name="concorda",
        ),
        migrations.RemoveField(
            model_name="chamado",
            name="presenca",
        ),
        migrations.RemoveField(
            model_name="chamado",
            name="shift",
        ),
        migrations.AddField(
            model_name="chamado",
            name="responsible_technician",
            field=models.CharField(
                blank=True,
                default="",
                max_length=100,
                verbose_name="Responsável técnico",
            ),
        ),
        migrations.AlterField(
            model_name="chamado",
            name="date",
            field=models.DateField(null=True, verbose_name="Data"),
        ),
        migrations.AlterField(
            model_name="chamado",
            name="equipment",
            field=models.CharField(max_length=100, verbose_name="Equipamento"),
        ),
        migrations.AlterField(
            model_name="chamado",
            name="obs",
            field=models.TextField(blank=True, null=True, verbose_name="Observações"),
        ),
        migrations.AlterField(
            model_name="chamado",
            name="requester",
            field=models.CharField(max_length=50, verbose_name="Solicitante"),
        ),
        migrations.AlterField(
            model_name="chamado",
            name="room",
            field=models.CharField(max_length=100, verbose_name="Sala"),
        ),
        migrations.AlterField(
            model_name="chamado",
            name="tombamento",
            field=models.CharField(max_length=100, verbose_name="Tombamento"),
        ),
    ]
