from django.core.paginator import Paginator
from django.conf import settings


class NmsPaginator(Paginator):
    def __init__(self, object_list, serializer_class=None, per_page=settings.PER_PAGE):
        self.serializer_class = serializer_class
        super().__init__(object_list, per_page)

    def get_objects(self, page):
        if int(page) < self.page_range.stop:
            return super().get_page(page).object_list
        else:
            return []

    def get_values(self, page):
        if int(page) < self.page_range.stop:
            return super().get_page(page).object_list.values()
        else:
            return []

    def get_data(self, page):
        if int(page) < self.page_range.stop and self.serializer_class:
            return self.serializer_class(super().get_page(page).object_list, many=True).data
        else:
            return []

    def get_max_page(self):
        return self.page_range.stop - 1
