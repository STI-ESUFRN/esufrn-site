from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ("laboratorio", "0005_add_ti_models"),  # Certifique-se de que a última migração criada está correta
    ]

    operations = [
        migrations.CreateModel(
            name="UserWarehouseTI",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("user", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, 
                    related_name="warehouses_ti", 
                    to="auth.User"
                )),
                ("warehouse_ti", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, 
                    related_name="responsibles_ti", 
                    to="laboratorio.WarehouseTI"
                )),
            ],
            options={
                "verbose_name": "Responsável (TI)",
                "verbose_name_plural": "Responsáveis (TI)",
                "unique_together": {("user", "warehouse_ti")},
            },
        ),
    ]
