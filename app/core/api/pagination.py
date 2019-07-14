from rest_framework.pagination import PageNumberPagination


class SmallPageNumberPagination(PageNumberPagination):
    page_size = 2
    max_page_size = 5
    page_size_query_param = 'page_size'


class StandardPageNumberPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 10
    page_size_query_param = 'page_size'


class LargePageNumberPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 50
    page_size_query_param = 'page_size'
