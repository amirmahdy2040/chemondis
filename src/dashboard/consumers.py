import copy
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class DashboardConsumer(AsyncJsonWebsocketConsumer):
    groups = set()

    async def connect(self):
        await self.accept()

    async def disconnect(self):
        groups = copy.deepcopy(self.groups)
        for group in groups:
            await self.unsubscribe_to_topic(group)

    async def receive_json(self, content):
        try:
            if content["type"] == "subscribe":
                await self.handle_subscription(content)
            elif content["type"] == "unsubscribe":
                await self.handle_unsubscription(content)
        except Exception as e:
            print(e)
            await self.send_json(
                {
                    "status": "failure",
                    "message": "Could not parse request or an error has occurred.",
                }
            )

    async def send_data(self, event):
        await self.send_json({"msg_type": event['msg_type'], "data": event['data']})

    async def add_to_group(self, group_name: str):
        await self.channel_layer.group_add(group_name, self.channel_name)
        self.groups.add(group_name)

    async def remove_from_group(self, group_name: str):
        await self.channel_layer.group_discard(group_name, self.channel_name)
        self.groups.remove(group_name)

    async def subscribe_to_topic(self, topic_name):
        await self.add_to_group(topic_name)
        for group in self.groups:
            await self.send_json(
                {
                    "status": "ok",
                    "city": topic_name,
                    "group": group,
                    "type": "subscription_result",
                }
            )

    async def unsubscribe_to_topic(self, topic_name):
        await self.remove_from_group(topic_name)

    async def handle_subscription(self, request):
        city = request["city"].replace(" ", "_")
        await self.subscribe_to_topic(city)

    async def handle_unsubscription(self, request):
        await self.disconnect()
