from rest_framework import mixins, viewsets


class RetriveListViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin,
                         mixins.ListModelMixin):
    pass
