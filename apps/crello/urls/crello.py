from apps.crello.views import (
    LabelReadOnlyViewset,
    LabelCUDViewset,
    BoardReadOnlyViewset,
    BoardCUDViewset,
    ListReadOnlyViewset,
    BoardListAllAPIView,
    BoardListDetailedAPIView,
    ChangeListPositionAPIView,
    ListCardAllAPIView,
    ListCardDetailedAPIView,
    CardAssigneeCUDAPIView,
    CardChangeOrderByPositionAPIView,
    CardImageUploadAPIView,
    CardFileUploadAPIView,
    CardCommentAllAPIView,
    CardCommentDetailedAPIView,
    Pattern,
)
from apps.common.router import router
from django.urls import path

app_name = "crello"

LABEL_URL_PREFIX = "api/labels/"
BOARD_URL_PREFIX = "api/boards/"
LIST_URL_PREFIX = "api/lists/"
CARD_URL_PREFIX = "api/cards/"

# Label
router.register(f"{LABEL_URL_PREFIX}read", LabelReadOnlyViewset)
router.register(f"{LABEL_URL_PREFIX}cud", LabelCUDViewset)

# Board
router.register(f"{BOARD_URL_PREFIX}read", BoardReadOnlyViewset)
router.register(f"{BOARD_URL_PREFIX}cud", BoardCUDViewset)

# List (read only)
router.register(f"{LIST_URL_PREFIX}read", ListReadOnlyViewset)

urlpatterns = [
    path("api/pattern/", Pattern.as_view(), name="print-pattern"),

    # Board to List - GET, POST
    path(f"{BOARD_URL_PREFIX}<int:board_id>/lists/", BoardListAllAPIView.as_view(), name="board_to_lists"),
    
    # Board to list - GET, PUT, PATCH, DELETE
    path(f"{BOARD_URL_PREFIX}<int:board_id>/lists/<int:list_id>/", BoardListDetailedAPIView.as_view(), name="board_to_lists_detail"),

    # Board to list - change order of the list - POST only
    path(f"{BOARD_URL_PREFIX}<int:board_id>/lists/<int:list_id>/change_position/<int:position>/", ChangeListPositionAPIView.as_view(), name="board_to_lists_change_position"),

    # List to card - GET, POST
    path(f"{LIST_URL_PREFIX}<int:list_id>/cards/", ListCardAllAPIView.as_view(), name="list_to_cards"),

    # List to card - GET, PUT, PATCH, DELETE
    path(f"{LIST_URL_PREFIX}<int:list_id>/cards/<int:card_id>/", ListCardDetailedAPIView.as_view(), name="list_to_cards_detail"),

    # List to card - add / update / remove assignee for the task - POST, DELETE
    path(f"{LIST_URL_PREFIX}<int:list_id>/cards/<int:card_id>/assignee/", CardAssigneeCUDAPIView.as_view(), name="card_change_assignee"),

    # change card order - b/w src & destn list - POST
    path(f"{LIST_URL_PREFIX}<int:list_id>/cards/<int:card_id>/move_list/<int:destn_list_id>/position/<int:position>/", CardChangeOrderByPositionAPIView.as_view(), name="change_card_src_to_destn"),

    # Card Image upload & delete - POST, DELETE
    path(f"{LIST_URL_PREFIX}<int:list_id>/cards/<int:card_id>/image_upload/", CardImageUploadAPIView.as_view(), name="card_image_uploader"),

    # Card File upload & delete - POST, DELETE
    path(f"{LIST_URL_PREFIX}<int:list_id>/cards/<int:card_id>/file_upload/", CardFileUploadAPIView.as_view(), name="card_file_uploader"),

    # Card to comment - GET, POST
    path(f"{CARD_URL_PREFIX}<int:card_id>/comments/", CardCommentAllAPIView.as_view(), name="card_comment"),

    # Card to comment - GET, POST, DELETE - get, modify, delete requested comment
    path(f"{CARD_URL_PREFIX}<int:card_id>/comments/<int:comment_id>/", CardCommentDetailedAPIView.as_view(), name="card_comment_detail"),

] 
urlpatterns += router.urls