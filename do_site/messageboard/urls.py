from django.urls import path
from .views import Messageboard, UserMessage

urlpatterns = [
    path('', Messageboard.as_view()),
    path('my_messages/', UserMessage.as_view()),
    path('my_messages/<int:pk>', UserMessage.as_view())
]