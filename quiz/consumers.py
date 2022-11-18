import json

import redis
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class QuizConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.counter_key = None
        self.quiz_pk = None
        self.room_group_name = None

    def connect(self):
        """Event when client connects"""
        # Informs client of successful connection
        self.quiz_pk = self.scope["url_route"]["kwargs"]["quiz_pk"]
        self.room_group_name = f"quiz_group_{self.quiz_pk}"
        self.counter_key = f"count:{self.room_group_name}"

        redis_client = redis.Redis(decode_responses=True)
        currently_connected = int(redis_client.get(self.counter_key) or 0)

        self.accept()

        self.send(
            text_data=json.dumps(
                {
                    "event": {
                        "type": "join",
                        "origin_channel": self.channel_name,
                        "payload": {"count": currently_connected},
                    }
                }
            )
        )

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        redis_client.set(self.counter_key, currently_connected + 1)

    def disconnect(self, close_code):
        """Event when client disconnects"""
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "join", "payload": {"count": -1}}
        )

        redis_client = redis.Redis(decode_responses=True)
        currently_connected = int(redis_client.get(self.counter_key) or 0)
        redis_client.set(self.counter_key, max(currently_connected - 1, 0))

    def receive(self, text_data):
        """Event when data is received"""
        text_data_json = json.loads(text_data)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, text_data_json
        )

    def join(self, event):
        origin_channel = event.pop("origin_channel", None)

        if origin_channel != self.channel_name:
            self.send(text_data=json.dumps({"event": event}))
