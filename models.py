from django.db import models
from django.contrib.auth.models import User
import os
import datetime



# Create your models here.



def getfilename(request,filename):
    now_time=datetime.datetime.now()
    new_file_name="%s%s"%(now_time,filename)
    return os.path.join('images/',new_file_name)


class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    password_token=models.CharField( max_length=500,null=True,blank=True)

    bio=models.TextField(max_length=100,blank=True,null=True)
    avator=models.ImageField(upload_to=getfilename,default="images/default.jpg",null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateField(auto_now=True)

    @property
    def image(self):
        if self.avator:
            return self.avator.url



class Room(models.Model):
    host=models.ForeignKey(User,on_delete=models.CASCADE,)
    name=models.CharField(max_length=30)
    topic=models.ForeignKey("Topic",on_delete=models.CASCADE)
    participants=models.ManyToManyField(User,related_name='participants',blank=True)
    description=models.TextField(max_length=300)
    updated=models.DateTimeField(auto_now=True,null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
   

    class Meta:
        ordering=['-updated','-created']

    def __str__(self):
        return self.name
    
class Message(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey('Room',on_delete=models.CASCADE)
    body=models.TextField(max_length=200)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['updated','created']


    def __str__(self):
        return self.body[0:50]

class Topic(models.Model):
   
    name=models.CharField(max_length=30)

    def __str__(self):
        return self.name

