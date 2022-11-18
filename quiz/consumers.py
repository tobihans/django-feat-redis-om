from channels.generic.websocket import WebsocketConsumer


class QuizConsumer(WebsocketConsumer):
    def connect(self):
        """Event when client connects"""
        # Informs client of successful connection
        self.accept()
        self.send(text_data="Welcome")

    def disconnect(self, close_code):
        """Event when client disconnects"""
        pass

    def receive(self, text_data):
        """Event when data is received"""
        pass
