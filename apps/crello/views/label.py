from rest_framework import status
from rest_framework.response import Response

from apps.common.views.generic import AppModelCUDAPIViewSet, AppModelListAPIViewSet
from apps.crello.models import Label
from apps.crello.serializers import LabelCUDSerializer, LabelDetailSerializer, LabelListSerializer


class LabelReadOnlyViewset(AppModelListAPIViewSet):
    queryset = Label.objects.active().order_by("id")
    serializer_class = LabelListSerializer

    def retrieve(self, request, *args, **kwargs):
        data = self.get_object()
        serializer = LabelDetailSerializer(instance=data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LabelCUDViewSet(AppModelCUDAPIViewSet):
    """CUD view for label object."""

    queryset = Label.objects.all()
    serializer_class = LabelCUDSerializer
