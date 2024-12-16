from apps.common.serializers import (
    AppReadOnlyModelSerializer,
    AppWriteOnlyModelSerializer
)
from apps.crello.models import (
    Card,
    ACCEPTABLE_FILE_EXTENSIONS,
    ACCEPTABLE_IMAGE_EXTENSIONS,
    ACCEPTABLE_IMAGE_MAX_MEMORY_SIZE,
)
from apps.access.serializers import (
    UserSerializer,
)
from .comment import CommentListSerializer
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

class CardImageUploadSerializer(serializers.ModelSerializer):
    class Meta():
        model = Card
        fields = ['card_image']

    def validate_card_image(self, image_upload):
        image_size = image_upload.size
        image_extension = image_upload.name.split('.')[-1]

        if image_size > ACCEPTABLE_IMAGE_MAX_MEMORY_SIZE:
            raise serializers.ValidationError("image size too big, upload within 5MB")
        
        if image_extension not in ACCEPTABLE_IMAGE_EXTENSIONS:
            raise serializers.ValidationError(f"unsupported image format, use only these formats --> {ACCEPTABLE_IMAGE_EXTENSIONS}")
        
        return image_upload

    def update(self, instance, validated_data):
        instance.card_image = validated_data.get('card_image', instance.card_image)
        instance.save()
        return instance

class CardFileUploadSerializer(serializers.ModelSerializer):
    class Meta():
        model = Card
        fields = ['card_file']

    def validate_card_file(self, file_upload):
        print(file_upload.name)
        file_extension = file_upload.name.split('.')[-1]
        print(file_extension)
        if file_extension not in ACCEPTABLE_FILE_EXTENSIONS:
            raise serializers.ValidationError(f"unsupported file format, use only these formats --> {ACCEPTABLE_FILE_EXTENSIONS}")
        
        return file_upload

    def update(self, instance, validated_data):
        instance.card_file = validated_data.get('card_file', instance.card_file)
        instance.save()
        return instance

class CardListSerializer(AppReadOnlyModelSerializer):
    assignee = UserSerializer(read_only=True)
    list_name = serializers.SerializerMethodField()
    label_name = serializers.SerializerMethodField()

    def get_list_name(self, obj):
        if obj.card_list:
            return obj.card_list.name
        return None

    def get_label_name(self, obj):
        if obj.label:
            return obj.label.name
        return None

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
    label_name = serializers.SerializerMethodField()
    list_name = serializers.SerializerMethodField()
    board_name = serializers.SerializerMethodField()
    comments = CommentListSerializer(many=True, read_only=True)

    def get_label_name(self, obj):
        if obj.label:
            return obj.label.name
        return None
    
    def get_list_name(self, obj):
        if obj.card_list:
            return obj.card_list.name
        return None
    
    def get_board_name(self, obj):
        if obj.card_list:
            if obj.card_list.board:
                return obj.card_list.board.name
        return None

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
            'comments',
        ]
