from apps.common.serializers import (
    AppReadOnlyModelSerializer,
    AppWriteOnlyModelSerializer
)
from apps.crello.models import (
    List,
)
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
    board_name = serializers.CharField(source='board.name')

    def get_cards_count(self, obj):
        return obj.cards.count()
    
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
    board_name = serializers.CharField(source='board.name')

    class Meta:
        model = List
        fields = [
            'id',
            'name',
            'position',
            'board_name',
            'created', 'modified',
        ]
        # incomplete, include card details as well
