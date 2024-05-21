from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import Service, Task, FormField, RequestField, StatusChoices
from .serializers import UserSerializer, ServiceSerializer, TaskSerializer, FormFieldSerializer, RequestFieldSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': response.data
        })


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class VerifyUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def get(self, request):
        user = request.user
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserServiceList(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Service.objects.filter(user_id=user_id)


class UserTasksList(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(client=self.request.user)

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

class Home(APIView):
    def get(self, request):
        data = {
            'message': "Welcome to our Django backend!",
            'status': "success"
        }
        return Response(data)


class ServiceList(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()


class ServiceFormFields(generics.ListCreateAPIView):
    serializer_class = FormFieldSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        service_id = self.kwargs['pk']
        return FormField.objects.filter(service_id=service_id)


class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]


class FormFieldList(generics.ListCreateAPIView):
    queryset = FormField.objects.all()
    serializer_class = FormFieldSerializer
    permission_classes = [permissions.IsAuthenticated]


class FormFieldDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FormField.objects.all()
    serializer_class = FormFieldSerializer
    permission_classes = [permissions.IsAuthenticated]


class RequestFieldList(generics.ListCreateAPIView):
    queryset = RequestField.objects.all()
    serializer_class = RequestFieldSerializer
    permission_classes = [permissions.IsAuthenticated]


class RequestFieldDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RequestField.objects.all()
    serializer_class = RequestFieldSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubmitRequest(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, service_id):
        service = get_object_or_404(Service, id=service_id)
        client = request.user
        task_data = {
            'service': service.id,
            'client': client.id,
            'req': request.data['req'],
            'status': StatusChoices.PENDING
        }
        task_serializer = TaskSerializer(data=task_data)
        if task_serializer.is_valid():
            task = task_serializer.save()
            for field_data in request.data.get('fields', []):
                form_field = FormField.objects.get(service=service, index=field_data['index'])
                RequestField.objects.create(
                    task=task,
                    type=field_data['type'],
                    value=field_data['value'],
                    index=field_data['index'],
                    options=field_data['options'],
                    prompt=form_field.prompt,  # Copy prompt
                    choices=form_field.choices  # Copy choices
                )
            return Response(task_serializer.data, status=status.HTTP_201_CREATED)
        return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateTaskStatus(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        new_status = request.data.get('status')
        if new_status not in dict(StatusChoices.choices):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        task.status = new_status
        task.save()

        return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)

class UserDetailWithServicesAndTasksView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)

        user_data = UserSerializer(user).data
        user_services = ServiceSerializer(Service.objects.filter(user=user), many=True).data
        user_tasks = TaskSerializer(Task.objects.filter(client=user), many=True).data

        data = {
            'user': user_data,
            'services': user_services,
            'tasks': user_tasks
        }

        return Response(data)