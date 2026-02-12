from rest_framework.pagination import PageNumberPagination

class StandardResultsPagination(PageNumberPagination):
    page_size_query_param = "page_size"

    def __init__(self, page_size=20, max_page_size=100):
        self.page_size = page_size
        self.max_page_size = max_page_size