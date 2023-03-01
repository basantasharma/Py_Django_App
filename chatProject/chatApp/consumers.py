from channels.consumer import AsyncConsumer, SyncConsumer
from channels.exceptions import StopConsumer
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