import os

from dotenv import load_dotenv

from .base import *  # noqa: F403
from .ckeditor import *  # noqa: F403

load_dotenv(override=True)

environment = os.getenv("ENVIRONMENT")

if environment == "PRODUCTION":
    print("## USING PRODUCTION ENVIRONMENT")  # noqa: T201
    from .production import *  # noqa: F403

elif environment == "HOMOLOGATION":
    print("## USING HOMOLOGATION ENVIRONMENT")  # noqa: T201
    from .homologation import *  # noqa: F403

else:
    print("## USING DEVELOPMENT ENVIRONMENT")  # noqa: T201
    from .development import *  # noqa: F403
