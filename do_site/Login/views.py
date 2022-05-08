import jwt
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from Login.models import User
from Login.renderers import UserJSONRenderer
from rest_framework.response import Response
from Login.serializers import RegistrationSerializer, LoginSerializer
from django.http import JsonResponse
from rest_framework import status
from do_site.settings import SECRET_KEY


class RegistrationAPIView(APIView):

    permission_classes = (AllowAny, )
    renderer_classes = (UserJSONRenderer, )
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user')
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user')
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)


def get_token(request):
    token = request.headers.get('Authorization')
    if token is not None:
        token = token.split()
        return token[1]
    return 0


def get_user(request):
    token = get_token(request)
    if token == 0:
        return 0
    payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms='HS256')
    return get_object_or_404(User.objects.all(), pk=payload.get('id'))
