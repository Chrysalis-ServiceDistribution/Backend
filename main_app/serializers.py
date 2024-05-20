from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Service, Task, FormField, TextFormField, RadioFormField, CheckboxFormField, RequestField, StatusChoices, FieldType, TextRequestField, RadioRequestField, CheckboxRequestField

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


class TextFormFieldSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return 'text'

    class Meta:
        model = TextFormField
        fields = ['type', 'prompt']


class RadioFormFieldSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return 'radio'

    class Meta:
        model = RadioFormField
        fields = ['type', 'prompt', 'choices']


class CheckboxFormFieldSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return 'checkbox'

    class Meta:
        model = CheckboxFormField
        fields = ['type', 'prompt', 'choices']


class ServiceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    form_fields = serializers.SerializerMethodField()

    def get_form_fields(self, obj):
        results = []
        for form_field in obj.form_fields:
            if form_field.type == 'text':
                return TextFormFieldSerializer(form_field.text_form_field)
            elif form_field.type == 'radio':
                return RadioFormFieldSerializer(form_field.radio_form_field)
            else:
                return CheckboxFormFieldSerializer(form_field.radio_form_field)
        return results

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


class RequestFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestField
        fields = ['id', 'task', 'type', 'value', 'index', 'options']


class TextRequestFieldSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return 'text'

    class Meta:
        model = TextRequestField
        fields = ['type', 'prompt']


class RadioRequestFieldSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return 'radio'

    class Meta:
        model = RadioRequestField
        fields = ['type', 'prompt', 'choices']


class CheckboxRequestFieldSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    def get_type(self, obj):
        return 'checkbox'

    class Meta:
        model = CheckboxRequestField
        fields = ['type', 'prompt', 'choices']


class TaskSerializer(serializers.ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    client = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    status = serializers.ChoiceField(choices=StatusChoices.choices, default=StatusChoices.PENDING)
    request_fields = serializers.SerializerMethodField()

    def get_request_fields(self, obj):
        results = []
        for request_field in obj.request_fields:
            if request_field.type == 'text':
                return TextRequestFieldSerializer(request_field.text_form_field)
            elif request_field.type == 'radio':
                return RadioRequestFieldSerializer(request_field.radio_form_field)
            else:
                return CheckboxRequestFieldSerializer(request_field.radio_form_field)
        return results

    class Meta:
        model = Task
        fields = ['id', 'service', 'client', 'req', 'status', 'request_fields']

    def create(self, validated_data):
        request_fields_data = validated_data.pop('request_fields', [])
        task = Task.objects.create(**validated_data)
        for request_field_data in request_fields_data:
            RequestField.objects.create(task=task, **request_field_data)
        return task
