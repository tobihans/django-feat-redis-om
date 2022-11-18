import json

import redis
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class QuizConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.quiz_pk = None
        self.room_group_name = None

    def connect(self):
        """Event when client connects"""
        # Informs client of successful connection
        self.quiz_pk = self.scope["url_route"]["kwargs"]["quiz_pk"]
        self.room_group_name = f"quiz_group_{self.quiz_pk}"

        redis_client = redis.Redis(decode_responses=True)
        key = f"count:{self.room_group_name}"
        currently_connected = int(redis_client.get(key) or 0)

        self.accept()

        self.send(
            text_data=json.dumps(
                {"event": {"type": "join", "payload": {"count": currently_connected}}}
            )
        )

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        redis_client.set(key, int(currently_connected + 1))

    def disconnect(self, close_code):
        """Event when client disconnects"""
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "join", "payload": {"count": -1}}
        )

    def receive(self, text_data):
        """Event when data is received"""
        text_data_json = json.loads(text_data)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, text_data_json
        )

    def join(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({"event": event}))
