import sys
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image


def resize_and_crop_image(uploaded_image, multiplier=1):
    dimension = 500
    name = {1: "", 2: "_medium", 3: "_low"}

    img_temp = Image.open(uploaded_image)
    img_temp = img_temp.convert("RGB")
    output_io_stream = BytesIO()
    width, height = img_temp.size
    smaller_edge = width if width < height else height

    left = (width - smaller_edge) / 2
    top = (height - smaller_edge) / 2
    right = (width + smaller_edge) / 2
    bottom = (height + smaller_edge) / 2
    img_temp_cropped = img_temp.crop((left, top, right, bottom))
    img_temp_resized = img_temp_cropped.resize(
        (dimension, dimension), Image.Resampling.LANCZOS
    )
    img_temp_resized.save(
        output_io_stream, format="JPEG", quality=int(100 / multiplier)
    )

    output_io_stream.seek(0)
    uploaded_image = InMemoryUploadedFile(
        output_io_stream,
        "ImageField",
        f"{uploaded_image.name.split('.')[0]}{name[multiplier]}.jpg",
        "image/jpeg",
        sys.getsizeof(output_io_stream),
        None,
    )
    return uploaded_image
