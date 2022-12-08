from django.db.models.signals import post_save
from django.dispatch import receiver

from reserva.helpers import notify_admin, notify_done, notify_requester
from reserva.models import Reserve


@receiver(post_save, sender=Reserve)
def notify_reserve(instance, created, **kwargs):
    if created:
        notify_admin(instance)
        notify_requester(instance)
        print("nay")

    elif (
        instance.status != Reserve.objects.get(id=instance.id).status
        and instance.status == Reserve.Status.APPROVED
    ):
        notify_done(instance)
