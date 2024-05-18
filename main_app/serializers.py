from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Service, Task, FormField, RequestField, StatusChoices, FieldType


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username']
        )
        return user


class ServiceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Service
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    client = UserSerializer(read_only=True)
    status = serializers.ChoiceField(choices=StatusChoices.choices, default=StatusChoices.PENDING)

    class Meta:
        model = Task
        fields = '__all__'


class FormFieldSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    type = serializers.ChoiceField(choices=FieldType.choices)
    choices = serializers.JSONField(required=False)

    class Meta:
        model = FormField
        fields = '__all__'


class RequestFieldSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)
    type = serializers.ChoiceField(choices=FieldType.choices)
    value = serializers.CharField(required=False)
    options = serializers.JSONField(required=False)

    class Meta:
        model = RequestField
        fields = '__all__'
