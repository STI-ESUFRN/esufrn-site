from django.apps import AppConfig


class AlmoxarifadoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "almoxarifado"

    def ready(self) -> None:
        import almoxarifado.signals  # noqa

        return super().ready()
