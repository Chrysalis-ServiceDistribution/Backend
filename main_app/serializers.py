from rest_framework import serializers
from .models import Service 
from .models import FormField
from .models import Task
from .models import RequestField 
from django.contrib.auth.models import User



class ServiceSerializer(serializers.ModelSerializer):
  class Meta:
    model = Service
    fiels = '__all__'



class FormfieldSerializer(serializers.ModelSerializer):
   class Meta:
    model = FormField
    fiels = '__all__'



class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fiels ='__all__'



class RequestFieldSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fiels = '__all__'



class UserSerializers(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'email', 'password', 'username')

    def create(self, validated_data):
      user = User.objects.create_user(
        email=validated_data['email'],
        password=validated_data['password'],
        username=validated_data['username']
      )

      return user


