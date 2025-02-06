from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ("laboratorio", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="WarehouseTI",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField("Nome (TI)", max_length=255)),
            ],
            options={
                "verbose_name": "Almoxarifado (TI)",
                "verbose_name_plural": "Almoxarifados (TI)",
            },
        ),
        migrations.CreateModel(
            name="MaterialTI",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField("Nome (TI)", max_length=255)),
                ("description", models.TextField("Descrição (TI)", blank=True, null=True)),
                ("brand", models.CharField("Marca (TI)", max_length=255, blank=True, null=True)),
                ("received_at", models.DateField("Recebido em (TI)", blank=True, null=True)),
                ("comments", models.TextField("Observações (TI)", blank=True, null=True)),
                ("qr_code", models.ForeignKey(
                    "assets.ESImage",
                    on_delete=models.PROTECT,
                    null=True,
                    editable=False,
                )),
                ("warehouse_ti", models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    to="laboratorio.WarehouseTI",
                    null=True, blank=True,
                    related_name="materials_ti_specific"
                )),
            ],
        ),
        migrations.CreateModel(
            name="ConsumableTI",
            fields=[
                ("materialti_ptr", models.OneToOneField(
                    auto_created=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    parent_link=True,
                    primary_key=True,
                    serialize=False,
                    to="laboratorio.MaterialTI"
                )),
                ("initial_quantity", models.IntegerField("Quantidade inicial", blank=True, null=True)),
                ("quantity", models.IntegerField("Quantidade disponível")),
                ("alert_below", models.IntegerField("Nível crítico")),
                ("expiration", models.DateField("Data de validade", blank=True, null=True)),
                ("sold_out_at", models.DateTimeField("Esgotado em", blank=True, null=True)),
            ],
            bases=("laboratorio.MaterialTI",),
        ),
    ]
