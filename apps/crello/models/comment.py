from django.db import models

from apps.common.models import COMMON_CHAR_FIELD_MAX_LENGTH, BaseModel
from apps.crello.models import Card


class Comment(BaseModel):
    """
    This model contains Comment details for a card.

    ********************* Model Fields *********************
        PK          - id
        Unique      - uuid
        FK          - created_by, modified_by, deleted_by, commented_by, card
        Datetime    - created, modified, deleted
        Boolean     - is_active, is_deleted
        CharField   - comment
    """

    comment = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    commented_by = models.CharField()

    class Meta:
        default_related_name = "related_card_comments"
