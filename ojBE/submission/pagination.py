from rest_framework.pagination import PageNumberPagination


class UserGetSubmissionListPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'size'
    page_query_param = 'page'