from django.db import models

from apps.common.models import COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG, COMMON_CHAR_FIELD_MAX_LENGTH, BaseModel
from apps.crello.models import Board


class List(BaseModel):
    """
    This model contains basic details about name.

    ********************* Model Fields *********************
        PK          - id
        Unique      - uuid
        FK          - created_by, modified_by, deleted_by, board
        Datetime    - created, modified, deleted
        Boolean     - is_active, is_deleted
        CharField   - identity
        TextField   - description
        PositiveInt - position
    """

    identity = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    description = models.TextField(**COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG)
    position = models.PositiveIntegerField(default=0)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG)

    class Meta:
        default_related_name = "related_lists"
