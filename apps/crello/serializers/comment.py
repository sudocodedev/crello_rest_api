from apps.common.serializers import (
    AppReadOnlyModelSerializer,
    AppWriteOnlyModelSerializer
)
from apps.crello.models import (
    Comment,
)
from apps.access.serializers import (
    UserSerializer,
)
from rest_framework import serializers

class CommentCUDSerializer(AppWriteOnlyModelSerializer):

    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = Comment
        fields = [
            'comment',
        ]

class CommentListSerializer(AppReadOnlyModelSerializer):
    commented_by = UserSerializer(read_only=True)
    card_name = serializers.SerializerMethodField()

    def get_card_name(self, obj):
        if obj.card:
            return obj.card.name
        return None

    class Meta:
        model = Comment
        fields = [
            'id',
            'comment',
            'commented_by',
            'card_name',
            'created',
            'modified',
        ]