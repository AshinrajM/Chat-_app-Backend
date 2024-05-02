from channels.generic.websocket import AsyncWebsocketConsumer


class PersonalChatconsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Testing connection & redis")
        await self.accept()
