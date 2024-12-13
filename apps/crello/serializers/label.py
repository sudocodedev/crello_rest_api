from apps.common.serializers import (
    AppReadOnlyModelSerializer,
    AppWriteOnlyModelSerializer
)
from apps.crello.models import (
    Label
)

class LabelListSerializer(AppReadOnlyModelSerializer):
    class Meta:
        model = Label
        fields = ['id','name',]

class LabelDetailSerializer(AppReadOnlyModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name', 'slug']

class LabelCUDSerializer(AppWriteOnlyModelSerializer):
    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = Label
        fields = ['name']
