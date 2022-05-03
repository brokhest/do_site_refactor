from django.urls import path
from .views import FileView, GetFile

urlpatterns = [
    path('', FileView.as_view()),
    path('<int:pk>', FileView.as_view()),
    path('download/<int:pk>', GetFile.as_view())
]