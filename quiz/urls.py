# from django.urls import path

from django.urls import path

from quiz import views

urlpatterns = [
    path("", views.index),
    path("create", views.create),
    path("quiz/<str:pk>", views.detail, name="quiz_detail"),
    path("quiz/<str:pk>/result", views.result, name="quiz_result"),
]
