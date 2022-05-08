from django.urls import path
from .views import Forum, UserMessage

urlpatterns = [
    path('', Forum.as_view()),
    path('my_messages/', UserMessage.as_view()),
    path('my_messages/<int:pk>', UserMessage.as_view())
]