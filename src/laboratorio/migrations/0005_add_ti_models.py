from django.db import migrations, models
import django.db.models.deletion
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('laboratorio', '0004_warehouseti_is_removed'),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoryTI",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name="created")),
                ("modified", model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name="modified")),
                ("quantity", models.IntegerField("Quantidade atualizada")),
                ("prev_quantity", models.IntegerField("Quantidade anterior", default=0)),
                ("item", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="history_ti", to="laboratorio.materialti")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="auth.user")),
            ],
            options={
                "verbose_name": "Histórico de material (TI)",
                "verbose_name_plural": "Histórico de materiais (TI)",
                "ordering": ["item__id", "-created"],
            },
        ),
        migrations.CreateModel(
            name="CategoryTI",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.TextField("Nome (TI)", max_length=255)),
                ("description", models.TextField("Descrição (TI)", null=True, blank=True)),
            ],
            options={
                "verbose_name": "Categoria (TI)",
                "verbose_name_plural": "Categorias (TI)",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="PermanentTI",
            fields=[
                ("materialti_ptr", models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to="laboratorio.materialti")),
                ("number", models.CharField("Tombamento", max_length=255, unique=True)),
                ("nserie", models.CharField("Número de série", max_length=255, null=True, blank=True)),
                ("modelo", models.CharField("Modelo", max_length=255, null=True, blank=True)),
                ("status", models.CharField(
                    "Status",
                    max_length=11,
                    choices=[("AVAILABLE", "Disponível"), ("UNAVAILABLE", "Indisponível")],
                    default="AVAILABLE",
                )),
                ("category", models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to="laboratorio.categoryti")),
            ],
            options={
                "verbose_name": "Material permanente (TI)",
                "verbose_name_plural": "Materiais permanentes (TI)",
                "ordering": ["name", "-created"],
            },
        ),
    ]
