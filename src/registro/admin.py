from django.contrib import admin
from .models import Pessoa, PessoaDeclaracao


class PessoaDeclaracaoInline(admin.StackedInline):
	model = PessoaDeclaracao
	extra = 0


@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
	list_display = (
		"numero",
		"saberes_competencias",
		"unidade_medida",
		"pontuacao",
		"solicitar_documentacao_chefia",
	"declaracoes_count",
		"created_at",
	)
	search_fields = ("saberes_competencias", "pessoas", "documentos_comprobatorios")
	list_filter = ("solicitar_documentacao_chefia",)
	readonly_fields = ("created_at", "updated_at")
	inlines = [PessoaDeclaracaoInline]

	def declaracoes_count(self, obj):
		return obj.declaracoes.count()
	declaracoes_count.short_description = "Decl." 
