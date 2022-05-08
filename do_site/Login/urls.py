from django.urls import path
from .views import RegistrationAPIView, LoginAPIView

urlpatterns = [
    path('register/', RegistrationAPIView.as_view()),
    path('', LoginAPIView.as_view())
]