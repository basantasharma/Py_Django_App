from channels.consumer import AsyncConsumer, SyncConsumer
from channels.exceptions import StopConsumer
import json
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer, AsyncWebsocketConsumer
#from channels.generic.websocket import AsyncWebsocketConsumer
#from asgiref.sync import async_to_sync
#from channels.generic.websocket import AsyncJsonWebsocketConsumer


class myAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("connected asyc basanta", event)
        await self.send({
            'type': "websocket.accept",
            "text": event,
            })
        #await self.accept()

    async def websocket_receive(self, event):
        print("recieved asyc basanta", event)
        await self.send({
            "type": "websocket.send",
            "text": "this is reply from server",#event['text'],
        })

    async def websocket_disconnect(self, event):
        print("disconnected asyc basanta", event)
        raise StopConsumer()





class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))










######################### SAMPLE FOR BUTTON ACCEPTING AND REJECTING CHAT ROOM ########################################

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Join the global lobby group
#         await self.channel_layer.group_add("lobby", self.channel_name)

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave the global lobby group
#         await self.channel_layer.group_discard("lobby", self.channel_name)

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         action = text_data_json["action"]

#         if action == "join":
#             # Join a specific room
#             room_name = text_data_json["room_name"]
#             room_group_name = f"chat_{room_name}"
#             await self.channel_layer.group_add(room_group_name, self.channel_name)

#             # Send a message to the room to inform other users
#             message = f"{self.scope['user'].username} has joined the room."
#             await self.channel_layer.group_send(
#                 room_group_name,
#                 {
#                     "type": "chat_message",
#                     "message": message,
#                 },
#             )
#         elif action == "leave":
#             # Leave the current room
#             room_name = text_data_json["room_name"]
#             room_group_name = f"chat_{room_name}"
#             await self.channel_layer.group_discard(room_group_name, self.channel_name)

#             # Send a message to the room to inform other users
#             message = f"{self.scope['user'].username} has left the room."
#             await self.channel_layer.group_send(
#                 room_group_name,
#                 {
#                     "type": "chat_message",
#                     "message": message,
#                 },
#             )

#     async def chat_message(self, event):
#         message = event["message"]

#         # Send the message to the WebSocket
#         await self.send(text_data=json.dumps({"message": message}))




















######################## SAMPLE FOR COUNTING NO. OF USERS ########################
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'chat_{self.room_name}'
#         self.waiting_room_group_name = f'waiting_{self.room_name}'

#         # Join the waiting room group
#         await self.channel_layer.group_add(
#             self.waiting_room_group_name,
#             self.channel_name,
#         )

#         # check the number of users in the waiting room
#         num_users = await self.channel_layer.group_send(
#             self.waiting_room_group_name,
#             {
#                 'type': 'count_users',
#             },
#         )

#         # if there is only one user in the waiting room, send a waiting message
#         if num_users == 1:
#             await self.send(text_data=json.dumps({
#                 'message': 'Waiting for more users to join...',
#             }))

#         # if there are at least two users in the waiting room, move them to the chat room
#         elif num_users >= 2:
#             # remove users from the waiting room
#             await self.channel_layer.group_discard(
#                 self.waiting_room_group_name,
#                 self.channel_name,
#             )
#             # join users to the chat room
#             await self.channel_layer.group_add(
#                 self.room_group_name,
#                 self.channel_name,
#             )
#             await self.accept()

#     async def disconnect(self, close_code):
#         # Leave the waiting room group
#         await self.channel_layer.group_discard(
#             self.waiting_room_group_name,
#             self.channel_name,
#         )

#         # Leave the chat room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name,
#         )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#             },
#         )

#     async def chat_message(self, event):
#         message = event['message']

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({
#             'message': message,
#         }))

#     async def count_users(self, event):
#         num_users = len(await self.channel_layer.group_channel_layer(
#             self.waiting_room_group_name
#         ).group_channels(self.waiting_room_group_name))
#         return num_users
