from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateUserView, LoginView, VerifyUserView, ServiceViewSet, TaskViewSet, FormFieldViewSet, RequestFieldViewSet, SubmitRequest, UpdateTaskStatus

router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'formfields', FormFieldViewSet)
router.register(r'requestfields', RequestFieldViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', CreateUserView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/verify/', VerifyUserView.as_view(), name='verify'),
    path('services/<int:service_id>/submit_request/', SubmitRequest.as_view(), name='submit_request'),
    path('tasks/<int:task_id>/update_status/', UpdateTaskStatus.as_view(), name='update_task_status'),
]