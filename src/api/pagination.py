from rest_framework.pagination import PageNumberPagination


class StdResultsSetPagination(PageNumberPagination):
    page_size = 8
    page_size_query_param = "page_size"
    max_page_size = 1000
