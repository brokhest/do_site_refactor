from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Message
from django.http import JsonResponse
from Login.views import get_user
from rest_framework import status
from rest_framework.generics import get_object_or_404
# Create your views here.


class Forum(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        data = []
        for message in Message.objects.all():
            record = {
                "text": message.text,
                "user": message.user.username
            }
            data.append(record)
        return JsonResponse(data, safe=False)


class UserMessage(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        user = get_user(request)
        text = request.data.get('text')
        message = Message(user=user, text=text)
        message.save()
        return Response(status=status.HTTP_201_CREATED)

    @staticmethod
    def get(request):
        user = get_user(request)
        data = []
        for message in user.messages.all():
            record = {
                "text": message.text,
                "pk": message.pk
            }
            data.append(record)
        return JsonResponse(data, safe=False)

    @staticmethod
    def delete(request, pk):
        user = get_user(request)
        message = get_object_or_404(user.messages.all(), pk=pk)
        message.delete()
        return Response(status=status.HTTP_200_OK)


