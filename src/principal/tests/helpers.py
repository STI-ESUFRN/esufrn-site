from typing import List

from model_bakery import baker

from principal.models import News, Newsletter, Page


def sample_news(**kwargs) -> News | List[News]:
    kwargs.setdefault("news", "")
    return baker.make(News, **kwargs)


def sample_page(**kwargs) -> Page | List[Page]:
    kwargs.setdefault("content", "")
    return baker.make(Page, **kwargs)


def sample_newsletter(**kwargs) -> Newsletter | List[Newsletter]:
    return baker.make(Newsletter, **kwargs)
