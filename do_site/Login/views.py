from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from Login.renderers import UserJSONRenderer
from rest_framework.response import Response
from Login.serializers import RegistrationSerializer, LoginSerializer
from django.http import JsonResponse
from rest_framework import status


class RegistrationAPIView(APIView):

    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)