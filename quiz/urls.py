# from django.urls import path

from django.urls import path

from quiz import views

urlpatterns = [path("", views.index), path("create", views.create), path("<str:pk>", views.detail, name="quiz_detail")]
