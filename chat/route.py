from django.urls import path
from .consusmers import PersonalChatconsumer


# just to identify it is for websocket routes
websocket_urlpatterns = [
    path("ws/chat/<int:id>/", PersonalChatconsumer.as_asgi()),
]
