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
        form_fields_data = self.request.data.get('form_fields', [])
        service = serializer.save(user=self.request.user)
        for form_field_data in form_fields_data:
            FormField.objects.create(service=service, **form_field_data)

class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        form_fields_data = self.request.data.get('form_fields', [])
        service = serializer.save()

        # Update or create form fields
        for form_field_data in form_fields_data:
            form_field_id = form_field_data.get('id')
            if form_field_id:
                form_field = FormField.objects.get(id=form_field_id, service=service)
                form_field.type = form_field_data.get('type', form_field.type)
                form_field.prompt = form_field_data.get('prompt', form_field.prompt)
                form_field.index = form_field_data.get('index', form_field.index)
                form_field.choices = form_field_data.get('choices', form_field.choices)
                form_field.save()
            else:
                FormField.objects.create(service=service, **form_field_data)

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
                RequestField.objects.create(task=task, **field_data)
            return Response(task_serializer.data, status=status.HTTP_201_CREATED)
        return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateTaskStatus(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        status = request.data.get('status')
        if status not in dict(StatusChoices.choices):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        task.status = status
        task.save()

        if status == StatusChoices.COMPLETED:
            # Perform any additional actions for completed tasks
            pass
        elif status == StatusChoices.CANCELLED:
            # Perform any additional actions for cancelled tasks
            pass

        return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)
