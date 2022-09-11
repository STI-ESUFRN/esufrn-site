from model_bakery import baker

from chamado.models import Chamado


def sample_chamado(**kwargs):
    return baker.make(Chamado, **kwargs)
