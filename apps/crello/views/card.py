from apps.common.views.base import (
    AppAPIView,
)
from apps.crello.serializers import (
    CardListSerializer, 
    CardDetailSerializer, 
    CardCUDSerializer, 
    CardImageUploadSerializer,
    CardFileUploadSerializer,
)
from apps.crello.models import (
    List, Board, Card, Label,
    PRIORITY,
)
from django.db.models import Max, F, Q
from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.common.helpers import (
    is_any_or_list1_in_list2,
    is_all_list1_in_list2,
)

User = get_user_model()

# helpers
card_payload_fields = ['name', 'description', 'priority', 'label', 'due_date']

def create_card(list_id:int, data:dict):
    priority = data.get('priority').lower()
    if priority not in PRIORITY:
        return -1

    label_instance = Label.objects.get_or_none(id=data.get('label'))
    if label_instance is None:
        return -2

    instance = List.objects.get_or_none(id=list_id)
    if instance is None:
        return -3

    # getting the maximum position among the cards that belonged to list object
    max_position = instance.cards.aggregate(mx_position=Max('position'))['mx_position'] or 0

    new_card = Card.objects.create(
        name=data.get('name'),
        description=data.get('description'),
        priority=priority,
        label=label_instance,
        position=max_position + 1,
        due_date=data.get('due_date'),
        card_list=instance,
    )

    return new_card

def delete_card(card_id:int) -> bool:
    instance = Card.objects.get_or_none(id=card_id)

    if instance is None:
        return False
    
    position = instance.position

    Card.objects.filter(position__gt=position).update(position=F('position')-1)
    instance.delete()
    return True

def get_assignee(data:dict):
    """
        return -> user object / None
    """
    
    try:
        assignee_id = int(data.get('assignee'))
        user = User.objects.get_or_none(id=assignee_id)

        if user is None:
            return None
                
    except ValueError as e:
        user_list = User.objects.filter(
            Q(email__iexact=data.get('assignee')) | 
            Q(phone_number=data.get('assignee'))
        )

        if len(user_list) == 0:
            return None
        user = user_list[0]
    
    return user

def move_card_to_other_list(card_id:int, src_list_id:int, destn_list_id, new_position:int) -> int:
    card_instance = Card.objects.get_or_none(id=card_id)
    if card_instance is None:
        return -1
    
    src_list_instance = List.objects.get_or_none(id=src_list_id)
    if src_list_instance is None:
        return -2
    
    destn_list_instance = List.objects.get_or_none(id=destn_list_id)
    if destn_list_instance is None:
        return -3
    
    src_position = card_instance.position
    max_position = destn_list_instance.cards.count()

    if new_position > max_position:
        new_position = max_position + 1

    elif new_position <= 0:
        new_position = 1
        
    destn_list_instance.cards.filter(position__gte=new_position).update(position=F('position')+1)
    src_list_instance.cards.filter(position__gt=src_position).update(position=F('position')-1)

    card_instance.position = new_position
    card_instance.card_list = destn_list_instance
    card_instance.save()

    return 1


class ListCardAllAPIView(AppAPIView):
    
    def get(self, request, *args, **kwargs):
        list_id = kwargs.get('list_id')
        instance = List.objects.get_or_none(id=list_id)
        
        if instance is None:
            return Response({'detail':"requested list doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        queryset = instance.cards.all()
        serializer = CardListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = request.data
        data_keys = list(data.keys())

        print(data_keys)
        print(is_all_list1_in_list2(card_payload_fields, data_keys))

        if not is_all_list1_in_list2(card_payload_fields, data_keys):
            return self.send_error_response({'detail': f"Invalid payload, not all params were present, refer {card_payload_fields}"})

        list_id = kwargs.get('list_id')
        
        queryset = create_card(list_id=list_id, data=data)
        if queryset == -1:
            return self.send_error_response({'detail': f"unsupported priority type, use these intead {PRIORITY}"})
        elif queryset == -2:
            return self.send_error_response({'detail': "provided label doesn't exist"})
        elif queryset == -3:
            return self.send_error_response({'detail': "requested list not found"})

        serializer = CardListSerializer(instance=queryset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ListCardDetailedAPIView(AppAPIView):

    def get(self, request, *args, **kwargs):
        list_id, card_id = kwargs.get('list_id'), kwargs.get('card_id')
        instance = List.objects.get_or_none(id=list_id)

        if instance is None:
            return Response({'detail':"requested list doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
        queryset = Card.objects.get_or_none(id=card_id, card_list=instance)

        if queryset is None:
            return Response({'detail':"requested card not found"}, status=status.HTTP_404_NOT_FOUND)


        serializer = CardDetailSerializer(instance=queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        data = request.data

        if not is_any_or_list1_in_list2(card_payload_fields, list(data.keys())):
            return self.send_error_response({'detail': f"Invalid params in payload, refer {card_payload_fields}"})
        
        card_id = kwargs.get('card_id')
        instance = Card.objects.get_or_none(id=card_id)

        if instance is None:
            return Response({'detail':"requested card doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CardCUDSerializer(instance, data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        data = request.data

        if not is_all_list1_in_list2(card_payload_fields, list(data.keys())):
            return self.send_error_response({'detail': f"Invalid params in payload, refer {card_payload_fields}"})

        card_id = kwargs.get('card_id')
        instance = Card.objects.get_or_none(id=card_id)

        if instance is None:
            return Response({'detail':"requested card doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        data['position'] = instance.position

        serializer = CardCUDSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        card_id = kwargs.get('card_id')
        res = delete_card(card_id=card_id)

        if res:
            return Response({'detail':"card deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        return self.send_error_response({'detail':"requested card doesn't exists"})
    

class CardAssigneeCUDAPIView(AppAPIView):
    """
    payload can be either user_id or email or phone_number
    param should be "assignee" only
    """

    def post(self, request, *args, **kwargs):
        data = request.data

        if 'assignee' not in data:
            return self.send_error_response({'detail': "Invalid param in payload"})
        
        user = get_assignee(data=data)
        if user is None:
            return Response({'detail': "requested user doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        card_id = kwargs.get('card_id')
        instance = Card.objects.get_or_none(id=card_id)

        if instance is None:
            return Response({'detail':"requested card doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
        instance.assignee = user
        instance.save()

        serializer = CardDetailSerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        card_id = kwargs.get('card_id')
        instance = Card.objects.get_or_none(id=card_id)

        if instance is None:
            return Response({'detail':"requested card doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
        instance.assignee = None
        instance.save()

        return Response({'detail': "assignee removed successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class CardChangeOrderByPositionAPIView(AppAPIView):

    def post(self, request, *args, **kwargs):
        position = kwargs.get('position')
        destn_list_id = kwargs.get('destn_list_id')
        card_id = kwargs.get('card_id')
        src_list_id = kwargs.get('list_id')

        res_code = move_card_to_other_list(card_id=card_id, src_list_id=src_list_id, destn_list_id=destn_list_id, new_position=position)

        if res_code == -1:
            return Response({'detail': "requested card doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        elif res_code == -2:
            return Response({'detail': "requested source list doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        elif res_code == -3:
            return Response({'detail': "requested destination list doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({'detail': "card moved successfully"}, status=status.HTTP_200_OK)

class CardImageUploadAPIView(APIView):
    serializer_class = CardImageUploadSerializer
    parser_classes = [MultiPartParser, FormParser,]

    def post(self, request, *args, **kwargs):
        data = request.data

        if 'card_image' not in data:
            return self.send_error_response({'detail': f"Invalid params in payload, use 'card_image'"})
        
        card_id = kwargs.get('card_id')
        instance = Card.objects.get_or_none(id=card_id)
        if instance is None:
            return Response({'detail': "requested card doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(instance=instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        card_id = kwargs.get('card_id')
        instance = Card.objects.get_or_none(id=card_id)
        if instance is None:
            return Response({'detail': "requested card doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        image_url = instance.card_image.url
        instance.card_image = None
        instance.save()

        return Response({'detail': f"{image_url} deleted successfully from card"}, status=status.HTTP_200_OK)
    

class CardFileUploadAPIView(APIView):
    serializer_class = CardFileUploadSerializer
    parser_classes = [MultiPartParser, FormParser,]

    def post(self, request, *args, **kwargs):
        data = request.data

        if 'card_file' not in data:
            return self.send_error_response({'detail': f"Invalid params in payload, use 'card_file'"})

        card_id = kwargs.get('card_id')        
        instance = Card.objects.get_or_none(id=card_id)
        if instance is None:
            return Response({'detail': "requested card doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(instance=instance, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, *args, **kwargs):
        card_id = kwargs.get('card_id')
        instance = Card.objects.get_or_none(id=card_id)
        if instance is None:
            return Response({'detail': "requested card doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        file_url = instance.card_file.url
        instance.card_file = None
        instance.save()

        return Response({'detail': f"{file_url} deleted successfully from card"}, status=status.HTTP_200_OK)

