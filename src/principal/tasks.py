from django.apps import apps

from esufrn.celery import app


@app.task(bind=True)
def publish_news(_, news_pk):
    news_model_cls = apps.get_model("principal", "News")
    try:
        news = news_model_cls.objects.get(pk=news_pk)

    except news_model_cls.DoesNotExist:
        return

    news.published = True
    news.save()
