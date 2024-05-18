from rest_framework import serializers
from .models import Service, Task, FormField, RequestField, StatusChoices, FieldType
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


    def create(self, validated_data):
      user = User.objects.create_user(
        email=validated_data['email'],
        password=validated_data['password'],
        username=validated_data['username']
      )

      return user

class ServiceSerializer(serializers.ModelSerializer):
  user =UserSerializer(read_only=True)
  class Meta:
    model = Service
    fiels = '__all__'


class TaskSerializer(serializers.ModelSerializer):
   service = ServiceSerializer(read_only=True)
   client = UserSerializer(read_only=True)
   status = serializers.ChoiceField(choices=StatusChoices.choices, default=StatusChoices.PENDING)

   class Meta:
      model = Task
      fiels = '__all__'
  

class FormfieldSerializer(serializers.ModelSerializer):
   service = ServiceSerializer(read_only=True)
   type = serializers.ChoiceField(choices=FieldType.choices)
   choice = serializers.JSONField(required=False)
   
   class Meta:
    model = FormField
    fiels = '__all__'


class RequestFieldSerializer(serializers.ModelSerializer):
  task = TaskSerializer(serializers.ModelSerializer)
  type =  serializers.ChoiceField(choices=FieldType.choices)
  value = serializers.CharField(requiered=False)
  options = serializers.JSONField(required=False)
  class Meta:
    model = RequestField
    fiels = '__all__'



