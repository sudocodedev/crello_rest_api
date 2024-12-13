from apps.common.views.generic import (
    AppModelCUDAPIViewSet,
    AppModelListAPIViewSet,
)
from apps.crello.serializers import (
    BoardCUDSerializer,
    BoardDetailSerializer,
    BoardListSerializer
)
from apps.crello.models import (
    Board,
)

from rest_framework.response import Response
from rest_framework import status

class BoardReadOnlyViewset(AppModelListAPIViewSet):
    queryset = Board.objects.all().order_by('id')
    serializer_class = BoardListSerializer

    def retrieve(self, request, *args, **kwargs):
        data = self.get_object()
        serializer = BoardDetailSerializer(instance=data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class BoardCUDViewset(AppModelCUDAPIViewSet):
    """
    for payload, use "name", "description"
    """
    queryset = Board.objects.all().order_by('id')
    serializer_class = BoardCUDSerializer