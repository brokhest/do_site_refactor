import mimetypes

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UploadSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .models import File
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from django.http import JsonResponse, HttpResponse
from todo.views import Get_user
from Login.models import User


def prepare_file(file):
    file_pointer = open(file.file.path, 'rb')
    file_type = mimetypes.guess_type(file.name)
    response = HttpResponse(file_pointer, content_type=file_type[0])
    response['Content-Disposition'] = 'attachment; filename=' + file.name
    return response

# Create your views here.


class FileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        user = Get_user(request)
        file_data = request.data.get('file')
        file = File(file=file_data, name=file_data.name, user=user, public=request.data.get('public'))
        file.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        user = Get_user(request)
        file = get_object_or_404(user.files.all(), pk=pk)
        file.delete()
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        user = Get_user(request)
        data = []
        for file in user.files.all():
            record = {
                'name': file.name,
                'size': file.file.size,
                'public': file.public,
                'permission': file.permission,
                'permissioned_to_user': file.permissioned_to,
                'keyword': file.keyword,
                'pk': file.pk}
            data.append(record)
        return JsonResponse(data, safe=False)

    def put(self, request, pk):
        user = Get_user(request)
        file = get_object_or_404(user.files.all(), pk=pk)
        if request.data.get('name'):
            file.name = request.data.get('name')
        if request.data.get('permission') is not None:
            file.permission = request.data.get('permission')
        if request.data.get('permissioned_to') is not None:
            file.permissioned_to = request.data.get('permissioned_to')
            file.keyword = request.data.get('keyword')
        if request.data.get('public') is not None:
            file.public = request.data.get('public')
        file.save()
        return Response(status=status.HTTP_200_OK)


class GetFile(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, pk):
        file = get_object_or_404(File.objects.all(), pk=pk)

        if file.public or file.user == Get_user(request):
            response = prepare_file(file)
            return response
        elif file.permission:
            if file.permissioned_to:
                if Get_user(request) and Get_user(request).username == file.keyword:
                    response = prepare_file(file)
                    return response
            else:
                print(request.data)
                if request.data.get('keyword') == file.keyword:
                    response = prepare_file(file)
                    return response
        return Response(status=status.HTTP_404_NOT_FOUND)
