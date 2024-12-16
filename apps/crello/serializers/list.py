from apps.common.serializers import (
    AppReadOnlyModelSerializer,
    AppWriteOnlyModelSerializer
)
from apps.crello.models import (
    List,
)
from .card import CardListSerializer
from rest_framework import serializers


class ListCUDSerializer(AppWriteOnlyModelSerializer):
    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = List
        fields = ['name',]

    def update(self, instance, validated_data):
        position = instance.position
        validated_data['position'] = position
        print(validated_data)
        
        return super().update(instance, validated_data)

class ListListSerializer(AppReadOnlyModelSerializer):
    cards_count = serializers.SerializerMethodField()
    board_name = serializers.SerializerMethodField()

    def get_cards_count(self, obj):
        return obj.cards.count()
    
    def get_board_name(self, obj):
        if obj.board:
            return obj.board.name
        return None
    
    class Meta:
        model = List
        fields = ['id', 'name', 
                  'position',
                  'board',
                  'board_name',
                  'cards_count',
                  'created', 'modified',
        ]

class ListDetailSerializer(AppReadOnlyModelSerializer):
    cards = CardListSerializer(many=True, read_only=True)
    board_name = serializers.SerializerMethodField()

    def get_cards_count(self, obj):
        return obj.cards.count()
    
    def get_board_name(self, obj):
        if obj.board:
            return obj.board.name
        return None

    class Meta:
        model = List
        fields = [
            'id',
            'name',
            'position',
            'board_name',
            'created', 'modified',
            'cards',
        ]
