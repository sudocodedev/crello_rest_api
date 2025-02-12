from django.db import models

from apps.common.models import COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG, COMMON_CHAR_FIELD_MAX_LENGTH, BaseModel


class Tag(BaseModel):
    """
    This model contains basic details about Tags.

    ********************* Model Fields *********************
        PK          - id
        Unique      - uuid
        FK          - created_by, modified_by, deleted_by,
        Datetime    - created, modified, deleted
        Boolean     - is_active, is_deleted
        CharField   - identity
    """

    identity = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH, **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG)

    class Meta:
        default_related_name = "related_tags"
