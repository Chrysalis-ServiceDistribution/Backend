from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import Home, CreateUserView, LoginView, VerifyUserView, ServiceViewSet, TaskViewSet, FormFieldViewSet, RequestFieldViewSet, SubmitRequest, UpdateTaskStatus


router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'formfields', FormFieldViewSet)
router.register(r'requestfields', RequestFieldViewSet)

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('users/register/', CreateUserView.as_view(), name='register'),
  path('users/login/', LoginView.as_view(), name='login'),
  path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
  path('service/<int:service_id>/submit_request/', SubmitRequest.as_view(), name='submit_request'),
  path('task/<int:task_id>/update_task/', UpdateTaskStatus.as_view(), name='update_task'),
  path('', include(router.urls)),

]