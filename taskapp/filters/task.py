from rest_framework.filters import SearchFilter

class TaskFilter(SearchFilter):
    search_param = 'status'
