from django.db import models

from apps.common.models import COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG, COMMON_CHAR_FIELD_MAX_LENGTH, BaseModel
from apps.crello.config import PriorityChoices
from apps.crello.models import Label, List, Tag


class Card(BaseModel):
    """
    This model contains basic details about Card.

    ********************* Model Fields *********************
        PK          - id
        Unique      - uuid
        FK          - created_by, modified_by, deleted_by, label, list
        Datetime    - created, modified, deleted
        Boolean     - is_active, is_deleted
        Choices     - priority
        CharField   - identity
        PositiveInt - position
        M2M         - tags
    """

    identity = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    position = models.PositiveIntegerField(default=0)
    list = models.ForeignKey(List, on_delete=models.CASCADE, **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG)
    tags = models.ManyToManyField(Tag, related_name="related_tags", **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG)
    label = models.ForeignKey(Label, on_delete=models.SET_DEFAULT, **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG)
    priority = models.CharField(
        choices=PriorityChoices.choices, max_length=COMMON_CHAR_FIELD_MAX_LENGTH, default=PriorityChoices.low
    )

    class Meta:
        default_related_name = "related_cards"
