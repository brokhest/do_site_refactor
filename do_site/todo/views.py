from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from Login.views import get_user
from .models import Task, Category
from rest_framework.response import Response


# Create your views here.


class Tasks(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        user = get_user(request)
        data = []
        for task in user.tasks.all():
            record = {
                "title": task.title,
                "description": task.desc,
                "completion": task.completion,
                'category': "None",
                "pk": task.pk
            }
            if task.category is not None:
                record.update({"category": task.category.name})
            data.append(record)
        return JsonResponse(data, safe=False)

    @staticmethod
    def post(request):
        user = get_user(request)
        task = Task(title=request.data.get('title'), desc=request.data.get('desc'),
                    user=user)
        task.save()
        return Response(status=status.HTTP_201_CREATED)

    @staticmethod
    def put(request, pk):
        user = get_user(request)
        task = get_object_or_404(user.tasks.all(), pk=pk)
        task.category = None
        if request.data.get('category') != "None":
            cat = get_object_or_404(user.categories.all(), name=request.data.get('category'))
            print(cat.name)
            task.category = cat
        task.title = request.data.get("title")
        task.desc = request.data.get("desc")
        task.completion = request.data.get("completion")
        task.save()
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, pk):
        user = get_user(request)
        task = get_object_or_404(user.tasks.all(), pk=pk)
        task.delete()
        return Response(status=status.HTTP_200_OK)


class Categories(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        user = get_user(request)
        data = []
        for cat in user.categories.all():
            record = {
                "name": cat.name,
                "Number of tasks": len(user.tasks.filter(category=cat))
            }
            data.append(record)
        return JsonResponse(data, safe=False)

    @staticmethod
    def post(request):
        user = get_user(request)
        if len(user.categories.filter(name=request.data.get('name'))) == 0:
            cat = Category(name=request.data.get('name'), user=user)
            cat.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_409_CONFLICT)

    @staticmethod
    def put(request, name):
        user = get_user(request)
        print(name)
        cat = get_object_or_404(user.categories.all(), name=name)
        if len(user.categories.filter(name=request.data.get('name'))) == 0:
            cat.name = request.data.get('name')
            cat.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_409_CONFLICT)

    @staticmethod
    def delete(request, name):
        user = get_user(request)
        cat = get_object_or_404(user.categories.all(), name=name)
        cat.delete()
        return Response(status=status.HTTP_200_OK)


class CategoryTasks(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, name):
        user = get_user(request)
        cat = get_object_or_404(user.categories.all(), name=name)
        data = []
        for task in user.tasks.all().filter(category=cat):
            record = {
                "title": task.title,
                "description": task.desc,
                "completion": task.completion,
                "pk": task.pk
            }
            data.append(record)
        return JsonResponse(data, safe=False)
