from django.db import migrations, models
import django.db.models.deletion


def forwards(apps, schema_editor):
    Sala = apps.get_model("chamado", "Sala")
    Chamado = apps.get_model("chamado", "Chamado")

    for chamado in Chamado.objects.exclude(room__isnull=True).exclude(room=""):
        sala, _ = Sala.objects.get_or_create(nome=chamado.room)
        chamado.sala = sala
        chamado.sala_outros = ""
        chamado.save(update_fields=["sala", "sala_outros"])


class Migration(migrations.Migration):

    dependencies = [
        ("chamado", "0006_refactor_chamado_new_ticket_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="Sala",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=100, unique=True, verbose_name="Sala")),
            ],
            options={
                "verbose_name": "Sala",
                "verbose_name_plural": "Salas",
                "ordering": ["nome"],
            },
        ),
        migrations.AddField(
            model_name="chamado",
            name="sala",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="chamados", to="chamado.sala", verbose_name="Sala"),
        ),
        migrations.AddField(
            model_name="chamado",
            name="sala_outros",
            field=models.CharField(blank=True, default="", max_length=100, verbose_name="Sala (outros)"),
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="chamado",
            name="room",
        ),
    ]
