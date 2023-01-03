from django.db.models.signals import post_save
from django.dispatch import receiver

from almoxarifado.models import History, MaterialInstance


@receiver(post_save, sender=MaterialInstance)
def create_log(sender, created, instance, **kwargs):
    if created:
        type = History.TypeChoices.ADDITION
    else:
        obj = MaterialInstance.objects.get(id=instance.id)
        if instance.quantity >= obj.quantity:
            type = History.TypeChoices.ADDITION
        else:
            type = History.TypeChoices.REMOVAL

    History.objects.create(
        instance=instance,
        quantity=instance.quantity,
        type=type,
    )
