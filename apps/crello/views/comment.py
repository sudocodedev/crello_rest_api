from apps.common.views.generic import (
    AppModelListAPIViewSet,
)
from apps.common.views.base import (
    AppAPIView,
)
from apps.crello.serializers import (
    CommentListSerializer, CommentCUDSerializer,
)
from apps.crello.models import (
    Comment, Card
)
from rest_framework.response import Response
from rest_framework import status

# helpers
def create_comment(card_id:int, comment:str, user):
    card = Card.objects.get_or_none1(id=card_id)
    if card is None:
        return None
    
    new_comment = Comment.objects.create(
        comment=comment,
        commented_by=user,
        card=card,
    )
    return new_comment
    

class CardCommentAllAPIView(AppAPIView):

    def get(self, request, *args, **kwargs):
        card_id = kwargs.get('card_id')
        instance = Card.objects.get_or_none1(id=card_id)
        if instance is None:
            return Response({'detail': "requested card doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        queryset = instance.comments.active()
        serializer = CommentListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = request.data
        user = self.get_user()

        if 'comment' not in data:
            return self.send_error_response({'detail': "Invalid param in payload, use 'comment'"})
        
        card_id = kwargs.get('card_id')

        queryset = create_comment(card_id=card_id, user=user, comment=data.get('comment'))
        if not queryset:
            return Response({'detail': "requested card doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommentListSerializer(instance=queryset)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CardCommentDetailedAPIView(AppAPIView):

    def get(self, request, *args, **kwargs):
        card_id = kwargs.get('card_id')
        comment_id = kwargs.get('comment_id')

        card_instance = Card.objects.get_or_none1(id=card_id)
        if card_instance is None:
            return Response({'detail': "requested card doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        queryset = Comment.objects.get_or_none1(id=comment_id, card=card_instance)
        if queryset is None :
            return Response({'detail': "comment not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentListSerializer(instance=queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        data = request.data

        if "comment" not in data:
            return self.send_error_response({'detail': "Invalid param in payload, use comment"})
        
        comment_id = kwargs.get('comment_id')

        
        instance = Comment.objects.get_or_none1(id=comment_id)
        if instance is None:
            return Response({'detail': "comment not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentCUDSerializer(instance=instance, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"detail": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, *args, **kwargs):
        comment_id = kwargs.get('comment_id')
        instance = Comment.objects.get_or_none1(id=comment_id)

        if instance is None:
            return Response({'detail': "comment not found"}, status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response({'detail': "comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        
    

