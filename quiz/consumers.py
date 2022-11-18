import json

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

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        """Event when client disconnects"""
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
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
