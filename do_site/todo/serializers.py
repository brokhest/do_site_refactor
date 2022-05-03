from rest_framework import serializers
from .models import Task, Category
from Login.models import User

class TaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(source='User', queryset=User.objects.all())
    category = serializers.PrimaryKeyRelatedField(source='Category', queryset=Category.objects.all())
    class Meta:
        model = Task
        fields = ('title', 'desc', 'completion', 'user', 'category')

    def create(self, user, **validated_data):
        #username = validated_data.get().username
        #task = Task(title=validated_data.get('title'), desc=validated_data.get('desc'), completion= validated_data.get('completion'), user=user)
        #return task

        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title')
        instance.desc = validated_data.get('desc')
        instance.completion = validated_data.get('completion')
        instance.category = validated_data.get('Category')
        instance.save()
        return instance
