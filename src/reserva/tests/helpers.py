from model_bakery import baker

from reserva.models import Period


def sample_period(**kwargs):
    return baker.make(Period, **kwargs)
