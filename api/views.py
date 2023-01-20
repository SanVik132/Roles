from django.shortcuts import render
from rest_framework.response import Response
from api.serializers import *
from rest_framework.mixins import ListModelMixin,CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import generics
from rest_framework import status
from django.contrib.auth import authenticate 
from api.create_token import get_tokens_for_user,get_user_from_token
from api.models import Task
from rest_framework.decorators import action,api_view
from rest_framework_simplejwt.tokens import RefreshToken,OutstandingToken,BlacklistedToken
from rest_framework.views import APIView



class RegistrationViewSet(CreateModelMixin,GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class LoginView(CreateModelMixin,GenericViewSet):
    serializer_class= LoginSerializer
    queryset=User.objects.all()
    
    def create(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            print('token',token)
            if user.is_active:
                dict = {'first_name':user.first_name,'last_name':user.last_name,'token':token,'email':user.email}
                return Response({'status':1,'message':'Logged in successfully','data':dict},status=status.HTTP_200_OK)
            
        return Response({'status':0,'message':'invalid Creds'})

class TaskCreateView(CreateModelMixin,GenericViewSet):
    serializer_class= TaskCreateSerializer
    queryset=Task.objects.all()

    def create(self,request):
        token = request.META.get("HTTP_AUTHORIZATION")
        user = get_user_from_token(token)
        if user:
            if user.has_perm('api.add_task'):
                serializer = self.serializer_class(data = request.data)
                if serializer.is_valid():
                    serializer.save(user = user)
                    return Response({'status':1,'message':'Task added','data':serializer.data},status=status.HTTP_200_OK)
                else:
                    return Response({'status':1,'message':'Errors','data':serializer.errors})
            else:
                return Response({'status':0,'message':'You are not permitted to add Task'})
        else:
            return Response({'status':0,'message':'Invalid User'})
    
    def delete(self,request,pk = None):
        token = request.META.get("HTTP_AUTHORIZATION")
        user = get_user_from_token(token)
        if user:
            if user.has_perm('api.delete_task'):
                pk = request.data.get('task_id')
                try:
                    Task.objects.get(id = pk).delete()
                    return Response({'status':1,'message':'Task Deleted'})
                except:
                    return Response({'status':0,'message':'Invalid Task Id'})

            else:
                return Response({'status':0,'message':'You are not permitted to Delete Task'})
        else:
            return Response({'status':0,'message':'Invalid User'})

    @action(methods=['put'], detail=False)
    def assign_task(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        user = get_user_from_token(token)
        if user:
            if user.has_perm('api.change_task'):
                pk = request.data.get('task_id')
                if pk:
                    try:
                        task = Task.objects.get(pk = pk)
                    except:
                        return Response({'status':0,'message':'Invalid Task id'})

                    serializer = TaskAssignSerializer(task,data = request.data)
                    if serializer.is_valid():
                        assigned_user = request.data.get('assigned_to')
                        try:
                            user = User.objects.get(pk = assigned_user,user_type =2)
                        except:
                            return Response({'status':0,'message':'Invalid Employess ID.'})
                        serializer.save()
                        return Response({'status':1,'message':'Task assigned','data':serializer.data},status=status.HTTP_200_OK)
                    else:
                        return Response({'status':1,'message':'Errors','data':serializer.errors})
                else:
                    return Response({'status':0,'message':'Invalid Task Id'})
            else:
                return Response({'status':0,'message':'You are not permitted to add Task'})
        else:
            return Response({'status':0,'message':'Invalid User'})

    @action(methods=['put'], detail=False)
    def complete_task(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        user = get_user_from_token(token)
        if user:
            if user.has_perm('api.change_task') and user.user_type == '2':
                pk = request.data.get('task_id')
                if pk:
                    try:
                        task = Task.objects.get(pk = pk)
                    except:
                        return Response({'status':0,'message':'Invalid Task id'})

                    serializer = TaskCompleteSerializer(task,data = request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'status':1,'message':'Task Completes','data':serializer.data},status=status.HTTP_200_OK)
                    else:
                        return Response({'status':1,'message':'Errors','data':serializer.errors})
                else:
                    return Response({'status':0,'message':'Invalid Task Id'})
            else:
                return Response({'status':0,'message':'You are not permitted to Complete Task'})
        else:
            return Response({'status':0,'message':'Invalid User'})



@api_view(['Get'])
def logout(request):
    print('hi')
    refresh_token  = request.META.get("HTTP_AUTHORIZATION")
    token = RefreshToken(refresh_token)
    token.blacklist()
    return Response(status=status.HTTP_205_RESET_CONTENT)