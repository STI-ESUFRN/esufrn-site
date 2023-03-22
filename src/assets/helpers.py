import sys
from enum import Enum
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image


class Quality(Enum):
    BEST = 1
    MEDIUM = 2
    WORSE = 3


def resize_image(uploaded_image, quality=Quality.BEST):
    name = {1: "", 2: "_medium", 3: "_low"}

    img_temp = Image.open(uploaded_image)
    img_temp = img_temp.convert("RGB")

    output_io_stream = BytesIO()
    img_temp.save(output_io_stream, format="JPEG", quality=int(100 / quality.value))

    output_io_stream.seek(0)
    return InMemoryUploadedFile(
        output_io_stream,
        "ImageField",
        f"{uploaded_image.name.split('.')[0]}{name[quality.value]}.jpg",
        "image/jpeg",
        sys.getsizeof(output_io_stream),
        None,
    )
