from rest_framework import serializers
from .models import Project, Task
from rest_framework import serializers
from .models import UserActivity

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(source='project.id', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)


    class Meta:
        model = Task
        fields = '__all__'



class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
