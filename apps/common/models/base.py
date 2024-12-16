import uuid
from contextlib import suppress

from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.core.files.base import ContentFile

from apps.common.managers import BaseObjectManagerQuerySet
from apps.common.models import (
    COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG,
    MAX_IMAGE_WIDTH,
    MAX_IMAGE_HEIGHT,
)
from apps.common.helpers import random_n_token


class ResizeImageMixin:
    def resize(self, image_field:models.ImageField):
        size = (MAX_IMAGE_HEIGHT, MAX_IMAGE_WIDTH,)
        
        im = Image.open(image_field) # getting original image
        im_format = image_field.name.split('.')[-1]
        im_name = image_field.name.split('.')[0]

        source_image = im.convert('RGB')
        source_image.thumbnail(size=size) # resizing the image

        output = BytesIO()
        source_image.save(output, format=im_format.upper())
        output.seek(0)

        content_file = ContentFile(output.read()) # read output from bytestream and create content file
        file = File(content_file)

        random_name = f"{im_name}_{random_n_token(5)}.{im_format}"
        image_field.save(random_name, file, save=False)


class BaseModel(models.Model):
    """
    Contains the last modified and the created fields, basically
    the base model for the entire app.

    ********************* Model Fields *********************
        PK          - id
        Unique      - uuid
        FK          - created_by, modified_by, deleted_by
        Datetime    - created, modified, deleted
        Boolean     - is_active, is_deleted
    """

    # UUID
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)

    # DateTime fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(**COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG)

    # ForeignKey fields
    created_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="created_%(class)s",
        on_delete=models.SET_DEFAULT,
        **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG,
    )
    updated_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="updated_%(class)s",
        on_delete=models.SET_DEFAULT,
        **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG,
    )
    deleted_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name="deleted_by_%(class)s",
        on_delete=models.SET_DEFAULT,
        **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG,
    )

    # Boolean fields
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    # custom manager
    objects = BaseObjectManagerQuerySet.as_manager()

    class Meta:
        abstract = True

    @classmethod
    def get_model_fields(cls):
        """
        Returns all the model fields. This does not
        include the defined M2M & related fields.
        """

        return cls._meta.fields

    @classmethod
    def get_all_model_fields(cls):
        """
        Returns all model fields, this includes M2M and related fields.
        Note: The field classes will be different & additional here.
        """

        return cls._meta.get_fields()

    @classmethod
    def get_model_field_names(cls, exclude=[]):  # noqa
        """Returns only the flat field names of the model."""

        exclude = ["id", "created_by", "created", "modified", *exclude]
        return [_.name for _ in cls.get_model_fields() if _.name not in exclude]

    @classmethod
    def get_model_field(cls, field_name, fallback=None):
        """Returns a single model field given by `field_name`."""

        with suppress(FieldDoesNotExist):
            return cls._meta.get_field(field_name)

        return fallback
