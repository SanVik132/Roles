from rest_framework import serializers
from api.models import User,Task
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    
    @staticmethod
    def validate_password(password: str) -> str:
        return make_password(password)
    class Meta:
        model = User
        fields = ['first_name','last_name','password','user_type','email','username']

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['pk','title','description','task_date']

class TaskAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['assigned_to']

class TaskCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status']