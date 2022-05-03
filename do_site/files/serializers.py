from rest_framework.serializers import Serializer, FileField, PrimaryKeyRelatedField
from .models import File
from Login.models import User

class UploadSerializer(Serializer):
    file = FileField()
    user = PrimaryKeyRelatedField(source='User', queryset=User.objects.all())
    class Meta:
        model = File
        fields = "__all__"

    def create(self, data ):
        file_data = data.get('file')
        file = File(file=file_data, name=file_data.name)
        return file
