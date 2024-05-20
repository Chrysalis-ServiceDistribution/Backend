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

class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ['id', 'type', 'prompt', 'index', 'choices']

class NestedFormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = ['id', 'type', 'prompt', 'index', 'choices']
        read_only_fields = ['id']

class RequestFieldSerializer(serializers.ModelSerializer):
    form_field = serializers.SerializerMethodField()

    class Meta:
        model = RequestField
        fields = ['id', 'task', 'type', 'value', 'index', 'options', 'form_field']

    def get_form_field(self, obj):
        form_field = FormField.objects.filter(service=obj.task.service, index=obj.index).first()
        if form_field:
            return FormFieldSerializer(form_field).data
        return None

class ServiceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    form_fields = NestedFormFieldSerializer(many=True)

    class Meta:
        model = Service
        fields = ['id', 'user', 'name', 'description', 'form_fields']

    def create(self, validated_data):
        form_fields_data = validated_data.pop('form_fields')
        service = Service.objects.create(**validated_data)
        for form_field_data in form_fields_data:
            FormField.objects.create(service=service, **form_field_data)
        return service

    def update(self, instance, validated_data):
        form_fields_data = validated_data.pop('form_fields', [])
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        # Clear existing form fields to prevent duplication
        instance.form_fields.all().delete()

        # Create new form fields
        for form_field_data in form_fields_data:
            FormField.objects.create(service=instance, **form_field_data)
        return instance

class TaskSerializer(serializers.ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    client = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    request_fields = RequestFieldSerializer(many=True, required=False)
    status = serializers.ChoiceField(choices=StatusChoices.choices, default=StatusChoices.PENDING)

    class Meta:
        model = Task
        fields = ['id', 'service', 'client', 'req', 'status', 'request_fields']

    def create(self, validated_data):
        request_fields_data = validated_data.pop('request_fields', [])
        task = Task.objects.create(**validated_data)
        for request_field_data in request_fields_data:
            RequestField.objects.create(task=task, **request_field_data)
        return task
