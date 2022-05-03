import jwt
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from Login.models import User
from .models import Task, Category
from rest_framework.response import Response
from .serializers import TaskSerializer
from do_site.settings import SECRET_KEY

# Create your views here.

def Get_token(request):
    token = request.headers.get('Authorization')
    if token is not None:
        token = token.split()
        return token[1]
    return 0



def Get_user(request):
    token = Get_token(request)
    if token == 0:
        return 0
    payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms='HS256')
    return get_object_or_404(User.objects.all(), pk=payload.get('id'))


class GetTask(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        user = Get_user(request)
        task = get_object_or_404(user.tasks.all(), pk=pk)
        record = {
            "title": task.title,
            "description": task.desc,
            "completion": task.completion,
            "pk": task.pk
        }
        return JsonResponse(record, safe=False)


class Tasks(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = Get_user(request)
        data = []
        for task in user.tasks.all():
                record = {
                    "title": task.title,
                    "description": task.desc,
                    "completion": task.completion,
                    'category': task.category.name,
                    "pk": task.pk
                }
                data.append(record)
        return JsonResponse(data, safe=False)

    def post(self, request):
        user = Get_user(request)
        data = request.data.get('task')
        # task ={
        #     "title": data['title'],
        #     "desc": data['desc'],
        #     "completion": data['completion'],
        #     "user": user.pk
        # }
        task = Task(title=data['title'], desc=data['desc'],
                    completion=data['completion'],
                    user=user)
        task.save()
        # serializer = TaskSerializer(user, data=task)
        # if serializer.is_valid(raise_exception=True):
        #     serializer.save()
        return Response({"success": "yes"})
        # return Response({"success":"no"})

    def put(self, request, pk):
        user = Get_user(request)
        task = get_object_or_404(user.tasks.all(), pk=pk)
        data = request.data.get('task')
        cat = get_object_or_404(user.categories.all(), name=data.get('category'))
        data.update({"category": cat.pk})
        serializer = TaskSerializer(instance=task, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"success": "yes"})
        return Response({"success": "no"})

    def delete(self, request, pk):
        user = Get_user(request)
        task = get_object_or_404(user.tasks.all(), pk=pk)
        task.delete()
        return Response({"success": "yes"})


class Categories(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = Get_user(request)
        data = []
        for cat in user.categories.all():
            record = {
                "name": cat.name,
                "Number of tasks": len(user.tasks.filter(category=cat))
            }
            data.append(record)
        return JsonResponse(data, safe=False)

    def post(self, request):
        user = Get_user(request)
        if len(user.categories.filter(name=request.data.get('name'))) == 0:
            cat = Category(name=request.data.get('name'), user=user)
            cat.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_409_CONFLICT)

    def put(self, request, name):
        user = Get_user(request)
        cat = get_object_or_404(user.categories.all(), name=name)
        cat.name = request.data.get('name')
        cat.save()
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, name):
        user = Get_user(request)
        cat = get_object_or_404(user.categories.all(), name=name)
        cat.delete()
        return Response(status=status.HTTP_200_OK)


class Category_tasks(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, name):
        user = Get_user(request)
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