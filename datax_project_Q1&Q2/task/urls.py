from rest_framework_nested import routers
from .views import ProjectViewSet, TaskViewSet

router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')

project_router = routers.NestedDefaultRouter(router, 'projects', lookup='project')
project_router.register('tasks', TaskViewSet, basename='project-tasks')

urlpatterns = router.urls + project_router.urls
