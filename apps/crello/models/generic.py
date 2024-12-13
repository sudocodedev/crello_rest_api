from django.db import models
from apps.common.models import (
    BaseModel,
    COMMON_CHAR_FIELD_MAX_LENGTH,
    COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG,
)
from django.template.defaultfilters import slugify
    
class Label(BaseModel):
    name = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH, blank=False, null=False)
    slug = models.SlugField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH, **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)