from django.apps import AppConfig


class ReservaConfig(AppConfig):
    name = "reserva"

    def ready(self) -> None:
        import reserva.signals  # noqa

        return super().ready()
