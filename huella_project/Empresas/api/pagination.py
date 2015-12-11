# -*- encoding: utf-8 -*-
from rest_framework.pagination import PageNumberPagination

__author__ = 'linglung'

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10