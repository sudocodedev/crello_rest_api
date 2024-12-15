from apps.common.views.generic import (
    AppModelListAPIViewSet,
)
from apps.common.views.base import (
    AppAPIView,
)
from apps.crello.serializers import (
    ListListSerializer, ListDetailSerializer, ListCUDSerializer
)
from apps.crello.models import (
    List, Board
)
from django.db.models import Max, F
from rest_framework.response import Response
from rest_framework import status
from apps.crello.tasks import print_pattern

class Pattern(AppAPIView):

    def get(self, request, *args, **kwargs):
        print_pattern.delay(iterations=10)
        return Response({'detail': "done"}, status=status.HTTP_200_OK)        

# helpers
def create_list(board_id:int, name:str):
    board = Board.objects.get(id=board_id)

    # getting the maximum position among the lists that belonged to the board object
    max_position = board.lists.aggregate(mx_position=Max('position'))['mx_position'] or 0

    new_list = List.objects.create(name=name, board=board, position=max_position + 1)
    return new_list

def delete_list(list_id:int) -> None:
    instance = List.objects.get(id=list_id)
    position = instance.position

    # update positions of the lists after list to be deleted
    List.objects.filter(position__gt=position).update(position=F('position')-1)
    instance.delete()

def change_list_position(list_id:int, new_position:int):
    instance = List.objects.get(id=list_id)
    current_position = instance.position
    
    if new_position < 1 or new_position > List.objects.count():
        return False
    
    if new_position < current_position:
        List.objects.filter(position__gte=new_position, position__lt=current_position).update(position=F('position')+1)
    elif new_position > current_position:
        List.objects.filter(position__gt=current_position, position__lte=new_position).update(position=F('position')-1)

    instance.position = new_position
    instance.save()

    return True

class ListReadOnlyViewset(AppModelListAPIViewSet):
    queryset = List.objects.all().order_by('id')
    serializer_class = ListListSerializer

    def retrieve(self, request, *args, **kwargs):
        data = self.get_object()
        serializer = ListDetailSerializer(instance=data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class BoardListAllAPIView(AppAPIView):

    def get(self, request, *args, **kwargs):
        board_id = kwargs.get('board_id')
        board = Board.objects.get_or_none(id=board_id)
        if board is None:
            return Response({'detail': "requested board doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
        queryset = board.lists.all()
        serializer = ListListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data

        # checking the payload params
        if 'name' not in data:
            return self.send_error_response({'detail': "Invalid param in payload"})

        board_id = kwargs.get('board_id')
        queryset = create_list(board_id=board_id, name=data.get('name'))
        serializer = ListListSerializer(instance=queryset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BoardListDetailedAPIView(AppAPIView):

    def get(self, request, *args, **kwargs):
        board_id = kwargs.get('board_id')
        list_id = kwargs.get('list_id')
        board = Board.objects.get_or_none(id=board_id)

        if board is None:
            return Response({'detail': "requested board doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
        queryset = List.objects.get_or_none(id=list_id, board=board)
        if queryset is None:
            return Response({'detail': "requested list doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ListDetailSerializer(instance=queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        data = request.data
        list_id = kwargs.get('list_id')

        if 'name' not in data:
            return self.send_error_response({'detail': "Invalid param in payload"})
        
        instance = List.objects.get_or_none(id=list_id)
        if instance is None:
            return Response({'detail': "requested list doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ListCUDSerializer(instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        data = request.data
        list_id = kwargs.get('list_id')

        if 'name' not in data:
            return self.send_error_response({'detail': "Invalid param in payload"})
        
        instance = List.objects.get_or_none(id=list_id)
        if instance is None:
            return Response({'detail': "requested list doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        data['position'] = instance.position

        serializer = ListCUDSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, *args, **kwargs):
        list_id = kwargs.get('list_id')
        delete_list(list_id=list_id)
        return Response({'detail':"list deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

class ChangeListPositionAPIView(AppAPIView):

    def post(self, request, *args, **kwargs):
        list_id = kwargs.get('list_id')
        position = kwargs.get('position')

        res = change_list_position(list_id=list_id, new_position=position)

        if not res:
            return self.send_error_response({'detail': "invalid position"})
        
        return Response({'detail':"list reordered successfully"}, status=status.HTTP_200_OK)
        



