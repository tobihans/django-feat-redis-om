from django.urls import re_path

from . import consumers

urlpatterns = [
    re_path(r"ws/quiz/(?P<quiz_pk>\w+)/$", consumers.QuizConsumer.as_asgi()),
]
