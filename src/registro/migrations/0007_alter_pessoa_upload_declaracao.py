from django.db import migrations, models
import uuid


def migrate_single_uploads(apps, schema_editor):
    Pessoa = apps.get_model('registro', 'Pessoa')
    PessoaDeclaracao = apps.get_model('registro', 'PessoaDeclaracao')
    # If the old field still exists in the DB (some backends keep column until removal op), copy values.
    # We access via getattr to avoid AttributeError if already dropped.
    for pessoa in Pessoa.objects.all():
        upload = getattr(pessoa, 'upload_declaracao', None)
        if upload:  # has a file
            PessoaDeclaracao.objects.create(pessoa=pessoa, arquivo=upload)


class Migration(migrations.Migration):

    dependencies = [
        ('registro', '0006_alter_pessoa_options_remove_pessoa_arquivo_and_more'),
    ]

    operations = []
    """No-op placeholder to resolve migration numbering conflict. Real changes are in 0009 and 0010."""