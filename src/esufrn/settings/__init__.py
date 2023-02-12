import os

from dotenv import load_dotenv

from .base import *  # noqa:
from .ckeditor import *  # noqa

load_dotenv(override=True)

environment = os.getenv("ENVIRONMENT")

if environment == "PRODUCTION":
    print("## USING PRODUCTION ENVIRONMENT")
    from .production import *  # noqa

elif environment == "HOMOLOGATION":
    print("## USING HOMOLOGATION ENVIRONMENT")
    from .homologation import *  # noqa

else:
    print("## USING DEVELOPMENT ENVIRONMENT")
    from .development import *  # noqa
