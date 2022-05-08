from django.urls import path
from .views import Tasks, CategoryTasks, Categories

urlpatterns = [
    path('task_list/by_category/<str:name>', CategoryTasks.as_view()),
    path('task_list/', Tasks.as_view()),
    path('task_list/<int:pk>', Tasks.as_view()),
    path('category/', Categories.as_view()),
    path('category/<str:name>', Categories.as_view())
]