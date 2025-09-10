from django.db import models
import uuid

class Pessoa(models.Model):
	numero = models.PositiveIntegerField("Nº")
	saberes_competencias = models.CharField("Saberes e Competências", max_length=255)
	descricao_item = models.TextField("Descrição do item", blank=True)
	documentos_comprobatorios = models.TextField("Documentos comprobatórios", blank=True)
	unidade_medida = models.CharField("Unidade de Medida", max_length=50, blank=True)
	pontuacao = models.DecimalField("Pontuação", max_digits=8, decimal_places=2, default=0)
	pessoas = models.CharField("Pessoas", max_length=255, blank=True)
	solicitar_documentacao_chefia = models.BooleanField("Solicitar documentação a chefia", default=False)
	observacoes = models.TextField("Observações", blank=True)
	uid = models.UUIDField("ID público", default=uuid.uuid4, editable=False, unique=True, db_index=True)
	created_at = models.DateTimeField("Criado em", auto_now_add=True)
	updated_at = models.DateTimeField("Atualizado em", auto_now=True)

	class Meta:
		ordering = ["numero"]

	def __str__(self):
		return f"{self.numero} - {self.saberes_competencias}"


class PessoaDeclaracao(models.Model):
	pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name="declaracoes")
	arquivo = models.FileField("Declaração", upload_to="arquivos_registro/")
	created_at = models.DateTimeField("Enviado em", auto_now_add=True)

	def __str__(self):
		return f"Declaração de {self.pessoa_id}"