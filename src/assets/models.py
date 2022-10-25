from django.db import models
from model_utils.models import TimeStampedModel

from assets.helpers import resize_and_crop_image


class ESImage(TimeStampedModel):
    image_high_url = models.ImageField(
        "Image (high)", blank=False, null=False, upload_to="images"
    )
    image_medium_url = models.ImageField(
        "Image (medium)", blank=True, null=True, upload_to="images"
    )
    image_low_url = models.ImageField(
        "Image (low)", blank=True, null=True, upload_to="images"
    )

    def save(self, *args, **kwargs):
        self.image_high_url = resize_and_crop_image(self.image_high_url, multiplier=1)
        self.image_medium_url = resize_and_crop_image(self.image_high_url, multiplier=2)
        self.image_low_url = resize_and_crop_image(self.image_high_url, multiplier=3)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created"]


class File(TimeStampedModel):
    url = models.FileField(upload_to="files")

    def __str__(self):
        return f"{self.created}"
