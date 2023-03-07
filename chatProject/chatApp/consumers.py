from channels.consumer import AsyncConsumer, SyncConsumer
from channels.exceptions import StopConsumer
import json
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
#from channels.generic.websocket import AsyncJsonWebsocketConsumer
# class mySyncConsumer(SyncConsumer):
#     def websocket_connect(self, event):
#         self.send({
#             'type': "websocket.accept"
#             })
#         print("connected sync", event)

#     def websocket_receive(self, event):
#         # self.send({
#         #     "type": "websocket.send",
#         #     "text": event["text"],
#         # })
#         print("recieved sync", event)

#     def websocket_disconnect(self, event):
#         print("disconnected sync", event)
#         #raise StopConsumer()

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


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))