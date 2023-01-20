from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import Permission



user_type_data = (('1', "Manager"), ('2', "Employee"), ('3', "Client"))
Status = (('pending','pending'),('complete','complete'))
# Create your models here.

class User(AbstractUser):
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)
    


class Task(models.Model):
    title  =  models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    task_date =  models.DateField()
    user = models.ForeignKey(User,related_name = 'created_by',on_delete = models.CASCADE,null = True,blank = True)
    status = models.CharField(default='pending', choices=Status, max_length=10)
    assigned_to = models.ForeignKey(User, on_delete = models.CASCADE,null = True,blank = True)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    
    if instance.user_type == '1':
        permission = Permission.objects.get(name='Can change task')
        permission1 = Permission.objects.get(name='Can delete task')
        instance.user_permissions.add(permission)
        instance.user_permissions.add(permission1)
    if instance.user_type == '2':
        permission = Permission.objects.get(name='Can change task')
        instance.user_permissions.add(permission)
    if instance.user_type == '3':
        permission = Permission.objects.get(name='Can add task')
        instance.user_permissions.add(permission)
