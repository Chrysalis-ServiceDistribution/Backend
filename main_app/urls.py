from django.urls import path
from .views import (
    Home,
    CreateUserView, LoginView, VerifyUserView,
    ServiceList, ServiceDetail, ServiceFormFields,
    TaskList, TaskDetail,
    FormFieldList, FormFieldDetail,
    RequestFieldList, RequestFieldDetail,
    SubmitRequest, UpdateTaskStatus
)

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('auth/register/', CreateUserView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/verify/', VerifyUserView.as_view(), name='verify'),

    path('services/', ServiceList.as_view(), name='service_list'),
    path('services/<int:pk>/', ServiceDetail.as_view(), name='service_detail'),
    path('services/<int:pk>/formfields/', ServiceFormFields.as_view(), name='service_formfields'),

    path('tasks/', TaskList.as_view(), name='task_list'),
    path('tasks/<int:pk>/', TaskDetail.as_view(), name='task_detail'),

    path('formfields/', FormFieldList.as_view(), name='formfield_list'),
    path('formfields/<int:pk>/', FormFieldDetail.as_view(), name='formfield_detail'),

    path('requestfields/', RequestFieldList.as_view(), name='requestfield_list'),
    path('requestfields/<int:pk>/', RequestFieldDetail.as_view(), name='requestfield_detail'),

    path('services/<int:service_id>/submit_request/', SubmitRequest.as_view(), name='submit_request'),
    path('tasks/<int:task_id>/update_status/', UpdateTaskStatus.as_view(), name='update_task_status'),
]
