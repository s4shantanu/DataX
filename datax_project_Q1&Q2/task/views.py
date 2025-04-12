from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from django.http import HttpResponse
import csv
from .serializers import UserActivitySerializer, ProjectSerializer, TaskSerializer
from .models import UserActivity, Project, Task
from .serializers import UserActivitySerializer, ProjectSerializer, TaskSerializer
from .utils import log_user_activity 



class UserActivityLogView(APIView):
    def get(self, request):
        logs = UserActivity.objects.all().order_by('-timestamp')
        serializer = UserActivitySerializer(logs, many=True)
        return Response(serializer.data)



class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = ProjectSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'start_date', 'end_date']

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        log_user_activity(request, f"Created project: {response.data.get('name')}")
        return response


    @action(detail=True, methods=['post'])
    def upload_image(self, request, pk=None):
        project = self.get_object()
        project.image = request.FILES.get('image')
        project.save()
        return Response({'status': 'image uploaded'})


    @action(detail=True, methods=['get'])
    def download_csv(self, request, pk=None):
        project = self.get_object()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="project_{project.id}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Description', 'Start Date', 'End Date', 'Duration'])
        writer.writerow([project.name, project.description, project.start_date, project.end_date, project.duration])
        return response


    @action(detail=False, methods=['post'])
    def bulk_delete(self, request):
        ids = request.data.get('ids', [])
        Project.objects.filter(id__in=ids).update(is_deleted=True)
        return Response({'status': 'Projects soft-deleted'})



class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_pk']
        return Task.objects.filter(project_id=project_id)
