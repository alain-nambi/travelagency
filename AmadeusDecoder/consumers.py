import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PnrConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("pnr_updates", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("pnr_updates", self.channel_name)

    async def receive(self, text_data):
        pass  # Pas besoin côté client pour l’instant

    async def send_pnr_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))
