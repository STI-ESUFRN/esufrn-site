from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from reserva.helpers import notify_admin, notify_done, notify_requester
from reserva.models import Reserve


@receiver(pre_save, sender=Reserve)
def notify_reserve_done(sender, instance, **kwargs):
    if not instance.pk or instance.status != Reserve.objects.get(id=instance.id).status:
        notify_done(instance)


@receiver(post_save, sender=Reserve)
def notify_reserve(sender, instance, created, **kwargs):
    if created:
        notify_admin(instance)
        notify_requester(instance)
