from apps.common.views.generic import (
    AppModelCUDAPIViewSet,
    AppModelListAPIViewSet,
)
from apps.crello.serializers import (
    LabelListSerializer, LabelCUDSerializer, LabelDetailSerializer
)
from apps.crello.models import (
    Label,
)

from rest_framework.response import Response
from rest_framework import status


class LabelReadOnlyViewset(AppModelListAPIViewSet):
    queryset = Label.objects.all().order_by('id')
    serializer_class = LabelListSerializer

    def retrieve(self, request, *args, **kwargs):
        data = self.get_object()
        serializer = LabelDetailSerializer(instance=data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LabelCUDViewset(AppModelCUDAPIViewSet):
    """
    for payload, use only "name"
    """
    queryset = Label.objects.all().order_by('id')
    serializer_class = LabelCUDSerializer
    