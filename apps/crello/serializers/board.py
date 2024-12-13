from apps.common.serializers import (
    AppReadOnlyModelSerializer,
    AppWriteOnlyModelSerializer
)
from apps.crello.models import (
    Board,
)
from apps.access.serializers import (
    UserSerializer,
)
from django.db.models import Count
from rest_framework import serializers

class BoardCUDSerializer(AppWriteOnlyModelSerializer):
    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = Board
        fields = ['name', 'description',]

class BoardListSerializer(AppReadOnlyModelSerializer):
    created_by = UserSerializer(read_only=True)
    lists_count = serializers.SerializerMethodField()
    cards_count = serializers.SerializerMethodField()

    def get_lists_count(self, obj):
        return obj.lists.count()
    
    def get_cards_count(self, obj):
        return obj.lists.all().aggregate(total_cards=Count('cards'))['total_cards']

    class Meta:
        model = Board
        fields = ['id','name', 
                  'description',
                  'created', 'modified',
                  'created_by',
                  'lists_count',
                  'cards_count',
        ] 

class BoardDetailSerializer(AppReadOnlyModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Board
        fields = [
            'id',
            'name',
            'description',
            'created_by',
            'created', 'modified',
        ]

        # not fully completed include list, card details as well in the serializer

