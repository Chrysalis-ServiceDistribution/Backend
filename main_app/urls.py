from django.urls import path
from .views import Home, CreateUserView, LoginView, VerifyUserView, ServiceViewSet, TaskViewSet, FormFieldViewSet, RequestFieldViewSet, SubmitRequest, UpdateTaskStatus

urlpatterns = [
  path('', Home.as_view(), name='home'),
  path('users/register/', CreateUserView.as_view(), name='register'),
  path('users/login/', LoginView.as_view(), name='login'),
  path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
  
]