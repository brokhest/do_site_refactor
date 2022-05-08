import mimetypes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from .models import File
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from django.http import JsonResponse, HttpResponse
from Login.views import get_user


def prepare_file(file):
    file_pointer = open(file.file.path, 'rb')
    file_type = mimetypes.guess_type(file.name)
    response = HttpResponse(file_pointer, content_type=file_type[0])
    response['Content-Disposition'] = 'attachment; filename=' + file.name
    return response

# Create your views here.


class FileView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    @staticmethod
    def post(request):
        user = get_user(request)
        file_data = request.data.get('file')
        file = File(file=file_data, name=file_data.name, user=user, public=request.data.get('public'))
        file.save()
        return Response(status=status.HTTP_201_CREATED)

    @staticmethod
    def delete(request, pk):
        user = get_user(request)
        file = get_object_or_404(user.files.all(), pk=pk)
        file.delete()
        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def get(request):
        user = get_user(request)
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

    @staticmethod
    def put(request, pk):
        user = get_user(request)
        file = get_object_or_404(user.files.all(), pk=pk)
        file.name = request.data.get("name")
        file.permission = request.data.get('permission')
        if file.permission:
            file.permissioned_to = request.data.get('permissioned_to')
            file.keyword = request.data.get('keyword')
        file.public = request.data.get('public')
        file.save()
        return Response(status=status.HTTP_200_OK)


class GetFile(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, FormParser)

    @staticmethod
    def get(request, pk):
        file = get_object_or_404(File.objects.all(), pk=pk)

        if file.public or file.user == get_user(request):
            response = prepare_file(file)
            return response
        elif file.permission:
            if file.permissioned_to:
                if get_user(request) and get_user(request).username == file.keyword:
                    response = prepare_file(file)
                    return response
            else:
                print(request.data)
                if request.data.get('keyword') == file.keyword:
                    response = prepare_file(file)
                    return response
        return Response(status=status.HTTP_404_NOT_FOUND)
