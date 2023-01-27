from django.conf import settings
from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = settings.REST_FRAMEWORK.get("PAGE_SIZE", 20)

    def paginate_queryset(self, queryset, request, view=None):
        if request.query_params.get("paginate", "true").lower() != "true":
            return None

        return super().paginate_queryset(queryset, request, view)
