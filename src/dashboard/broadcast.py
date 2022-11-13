from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def broadcast(city: str, data: dict):
    city = city.replace(" ", "_")
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(city, {"type": "send_data", "msg_type": "city", "data": data}, )
