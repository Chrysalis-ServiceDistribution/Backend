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


class ServiceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    form_fields = FormFieldSerializer(many=True)

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
        form_fields_data = validated_data.pop('form_fields')
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        # Update or create form fields
        for form_field_data in form_fields_data:
            form_field_id = form_field_data.get('id')
            if form_field_id:
                form_field = FormField.objects.get(id=form_field_id, service=instance)
                form_field.type = form_field_data.get('type', form_field.type)
                form_field.prompt = form_field_data.get('prompt', form_field.prompt)
                form_field.index = form_field_data.get('index', form_field.index)
                form_field.choices = form_field_data.get('choices', form_field.choices)
                form_field.save()
            else:
                FormField.objects.create(service=instance, **form_field_data)
        return instance


class RequestFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestField
        fields = ['id', 'task', 'type', 'value', 'index', 'options']


class TaskSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    client = UserSerializer(read_only=True)
    status = serializers.ChoiceField(choices=StatusChoices.choices, default=StatusChoices.PENDING)

    class Meta:
        model = Task
        fields = '__all__'
