from django.db import models
from django.contrib.auth import get_user_model
from apps.common.models import (
    BaseModel,
    COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG,
    COMMON_CHAR_FIELD_MAX_LENGTH
)
from .config import PriorityType
from .generic import Label

User = get_user_model()

class Board(BaseModel):
    name = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH, blank=False, null=False)
    description = models.TextField(**COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG)

    def __str__(self):
        return f"{self.name} by {self.created_by.username}"
    
class List(BaseModel):
    name = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH, 
                            blank=False, null=False
    )
    position = models.PositiveIntegerField()
    
    board = models.ForeignKey(Board, 
                              on_delete=models.CASCADE, 
                              null=False, blank=False, 
                              related_name="lists"
    )

    class Meta:
        ordering = ['position',]

    def __str__(self):
        return f"{self.name} -> Board: {self.board.name}"
    
class Card(BaseModel):
    name = models.CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH, 
                            blank=False, null=False
    )
    description = models.TextField(**COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG)
    position = models.PositiveIntegerField()
    due_date = models.DateField()
    
    ## media fields
    card_image = models.ImageField(upload_to="card-images/%Y/%m/", 
                              **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG
    )
    card_file = models.FileField(upload_to="card-files/%Y/%m/",
                            **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG
    )


    ## choice field
    priority = models.CharField(choices=PriorityType, 
                                default=PriorityType.low, 
                                max_length=COMMON_CHAR_FIELD_MAX_LENGTH
    )
    
    ## Foreign key fields
    card_list = models.ForeignKey(List,
                                  related_name="cards",
                                  on_delete=models.SET_DEFAULT, 
                                  **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG
    )

    assignee = models.ForeignKey(User, 
                                 related_name="assigned_tasks", 
                                 on_delete=models.SET_DEFAULT, 
                                 **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG
    )

    label = models.ForeignKey(Label, 
                              related_name="used_in_tasks", 
                              on_delete=models.SET_DEFAULT, 
                              **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG
    )

    class Meta:
        ordering = ['position',]

    def __str__(self):
        return f"{self.name} -> List: {self.card_list.name} -> Board: {self.card_list.board.name}"
    

class Comment(BaseModel):
    comment = models.TextField(null=False, blank=False)

    ## foreign key fields
    commented_by = models.ForeignKey(User, 
                                 related_name="comments", 
                                 on_delete=models.SET_DEFAULT, 
                                 **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG
    )

    card = models.ForeignKey(Card, 
                             related_name="comments", 
                             on_delete=models.SET_DEFAULT, 
                             **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG
    )