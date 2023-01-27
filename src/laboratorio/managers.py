from model_utils.models import SoftDeletableManager


class ConsumableManager(SoftDeletableManager):
    def get_queryset(self):
        return super().get_queryset().filter(quantity__gt=0)
