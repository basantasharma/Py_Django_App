from django.urls import path
from . import consumers
websocket_urlpatterns = [
    #path('ws/sc/', consumers.mySyncConsumer.as_asgi()),
    path('ws/ac/', consumers.myAsyncConsumer.as_asgi()),
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]