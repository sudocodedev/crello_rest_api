from apps.common.serializers import (
    AppReadOnlyModelSerializer,
    AppWriteOnlyModelSerializer
)
from apps.crello.models import (
    Card,
)
from apps.access.serializers import (
    UserSerializer,
)
from rest_framework import serializers

class CardCUDSerializer(AppWriteOnlyModelSerializer):

    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = Card
        fields = [
            'name',
            'description',
            'priority',
            'label',
            'due_date',
        ]

class CardImageUploadSerializer(AppWriteOnlyModelSerializer):
    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = Card
        fields = ['card_image']

class CardListSerializer(AppReadOnlyModelSerializer):
    assignee = UserSerializer(read_only=True)
    list_name = serializers.CharField(source='card_list.name')
    label_name = serializers.CharField(source='label.name')

    class Meta:
        model = Card
        fields = [
            'id',
            'name',
            'position',
            'priority',
            'assignee',
            'label_name',
            'list_name',
            'created', 'modified',
        ]

class CardDetailSerializer(AppReadOnlyModelSerializer):
    assignee = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    label_name = serializers.CharField(source='label.name')
    list_name = serializers.CharField(source='card_list.name')
    board_name = serializers.CharField(source="card_list.board.name")

    class Meta:
        model = Card
        fields = [
            'id',
            'name',
            'description',
            'position',
            'priority',
            'label_name',
            'due_date',
            'created_by',
            'created', 'modified',
            'assignee',
            'card_image',
            'card_file',
            'board_name',
            'list_name',
        ]
