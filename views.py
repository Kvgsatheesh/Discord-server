from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.core.mail import send_mail
import uuid
from django.conf import settings
import random



# Create your views here.

def loginpageview(request):
    page='login'
    if request.user.is_authenticated:

        return redirect('base:home')
    
    if request.method=='POST':
        username=request.POST['username'].lower()
        password=request.POST['password']
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'user does not exists')

        user=authenticate(request,username=username,password=password)
        if user is not None:
                login(request,user)
                return redirect('base:home')
        else:
            messages.error(request,'credntial error')   
    context={'page':page}
    return render(request,'base/loginreg.html',context)

def logoutpageview(request):
    logout(request)
    return redirect('base:home')


def signup(request):
    page='signup'
    form=signupform()
    if request.method=='POST':
        form=signupform(request.POST)
    
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            if user.username is  not None:
                user.save()
                return redirect('base:login')  
            
        else:
            messages.error(request,'error')
    
    
    context={'form':form,'page':page}
    return render(request,'base/loginreg.html',context)



def home(request):
    q=request.GET.get('q') if request.GET.get('q') !=None else ''
    rooms=Room.objects.filter(
       Q(topic__name__icontains=q) |
       Q(name__icontains=q) |
       Q(description__icontains=q) |
       Q(host__username__icontains=q)
    ).order_by('-updated','-created')
    
    ra=Message.objects.all().order_by('-updated','-created')
    topics=Topic.objects.all()

    
    profile=Profile.objects.all()
    
    context={'rooms':rooms,'topic':topics,'allmsg':ra,'profile':profile}
    return render(request,'base/home.html',context)



def room(request,id):
    room=Room.objects.get(id=id)
    msg=room.message_set.all().order_by('-updated','-created')
    participant=room.participants.all()
    
    
    if (request.method=='POST'):
        newmsg=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        
            
    context={'room':room,'msg':msg,'participant':participant}
    return render(request,'base/room.html',context)



def updateroom(request,id):
    item=Room.objects.get(id=id)
    form=Roomform(instance=item)
    if request.user != item.host:
        return HttpResponse('access deneid')
    if request.method=='POST':
        form=Roomform(request.POST,instance=item)
        if form.is_valid(): 
            form.save()
            return redirect('base:home')
    return render(request,'base/room_form.html',{'form':form})




def deleteroom(request,id):
    room=Room.objects.get(id=id)
    if (request.user != room.host):
        return HttpResponse('access deneid')
    
    if (request.user == room.host) | (request.user.is_superuser):
        if request.method=='POST':
            room.delete()
            
            return redirect('base:home')
    return render(request,'base/delete.html',{'obj':room})

def deletemessage(request,mid,rid):
    msg=Message.objects.get(id=mid)   
    room=Room.objects.get(id=rid)

    if request.method=='POST':
        if (request.user == msg.user) | (request.user.is_superuser) | (request.user == room.host):
            msg.delete()
            
            return redirect('base:room',id=room.id)
        else:
            messages.error(request,'not allowed')
    return render(request,'base/delete.html',{'obj':msg})


def adeletemessage(request,mid):
    msg=Message.objects.get(id=mid)   
    if request.method=='POST':
        if (request.user == msg.user) | (request.user.is_superuser) | (request.user == msg.room.host):
            msg.delete()
            
            return redirect('base:home')
        else:
            messages.error(request,'not allowed')
    return render(request,'base/delete.html',{'obj':msg})

def userprofile(request,id):
    
    user=User.objects.get(id=id)
   
   
    try:
        pro=Profile.objects.get(user_id=id)
    except:
        pro=None



    rooms=user.room_set.all().order_by('-updated','-created')

    msg=user.message_set.all().order_by('-updated','-created')
    topic=Topic.objects.all()
    
    context={'user':user,'rooms':rooms,'allmsg':msg,'topic':topic,'pro':pro}
    return render(request,'base/profile.html',context)
   

def updateuser(request):
    user=User.objects.get(id=request.user.id)
    
    form=userupdate(instance=user)
    try:
        pro=Profile.objects.get(user_id=request.user.id)
       
        form2=updateuser2(instance=pro)
    
       
    except:
        
        form2=updateuser2()
        if request.method=='POST':
            form=userupdate(request.POST or None, request.FILES or None,instance=user)
            form.save()

            form2=updateuser2(request.POST or None, request.FILES or None)

            createprofile=form2.save(commit=False)
            createprofile.user=request.user
            createprofile.save()
            
            return redirect('base:profile',id=user.id)
        return render(request,'base/updateprofile.html',{'form':form,'form2':form2})
    


    if request.method=='POST':
            form=userupdate(request.POST or None, request.FILES or None,instance=user)
            form2=updateuser2(request.POST or None, request.FILES or None,instance=pro)
            
            if form.is_valid() & form2.is_valid():
                form.save()
            
                form2.save()
                return redirect('base:profile',id=user.id)
            else:
                messages.error('error occur')


                
    return render(request,'base/updateprofile.html',{'form':form,'form2':form2})


   
    

def updatemessage(request,id,rid):
    msg=Message.objects.get(id=id)
    room=Room.objects.get(id=rid)
    
    if request.user == msg.user:
        if request.method=='POST':
            updatemsg=Message.objects.get(id=id)
            (updatemsg.body)=request.POST.get('body')
            updatemsg.save()
            return redirect('base:room',id=room.id)
    return render(request,'base/update-message.html',{'msg':msg})
    


@login_required(login_url='/login')
def createroom(request):   
    form=Roomform()
    if request.method=='POST':
        form=Roomform(request.POST)
        if form.is_valid():
           user=form.save(commit=False)
           user.host=request.user
           form.save()       
        return redirect('base:home')    
    context={'form':form}
    return render(request,'base/room_form.html',context)


    
@login_required(login_url='/login')
def addtopic(request):
    form=addtopicform()
    if request.method=='POST':
        new_topic=request.POST['name'].lower()
        topic=Topic.objects.get_or_create(name=new_topic)
        return redirect('base:home')
    return render(request,'base/addtopic.html',{'form':form})
            

class PasswordsChangeView(PasswordChangeView):
    form_class=passwordchangingform
    
    success_url=reverse_lazy('base:password_success')

    
def password_success(request):
    return render(request,'base/password_success.html')
 


def passwordreset(request):
    form=pwresetform()
    if request.method == "POST":
        
        name=request.POST['username'].lower()

        try:
        
            if User.objects.get(username=name):
                token=str(uuid.uuid4())
                
                user=User.objects.get(username=name)
                email=user.email
                try:
                    pro=Profile.objects.get(user_id=user.id)
                    pro.password_token=token
                    pro.save()
                    
                except:
                     Profile.objects.create(
                    user=user,
                    password_token=token

                )
                    
                send_mail(
                    subject="your password reset link",
                    message= f'( hi click the link to reset your password http://127.0.0.1:8000/setpassword/{token}/{user.id} )',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email]
                    )
                messages.error(request,'mail sent')
                
        except:
                messages.error(request,'user does not exists')

    return render(request,'base/resetpw.html',{'form':form})


def setpassword(request,token,id):
    form=pwreset()
   
    if request.method == 'POST':
        
        form=pwreset(request.POST)
        
        try:
            if Profile.objects.get(password_token = token):
                
                pw=request.POST['password']
                cpw=request.POST['confirm_password']
                if pw == cpw:
                    
                    user=User.objects.get(id=id)
                
                    user.set_password(pw)
                    user.save()
                    pro=Profile.objects.get(password_token = token)
                    pro.password_token= None
                    pro.save()
                    return redirect('base:login')
                else:
                    messages.error(request,'password not match')

        except:
            messages.error(request,'link not available')
           

    return render(request,'base/setpassword.html',{'form':form})
        

def otpverify(request):
    form=otpform()
    if request.method == 'POST':
        otp=request.POST['otp']
        try:
        
            if Profile.objects.get(password_token = otp):
                
                pro=Profile.objects.get(password_token = otp)
                
                user_id=pro.user.id
                user=User.objects.get(id=user_id)
                pro.password_token = None
                pro.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('base:home')
        except:   
        
            messages.error(request,'invalid otp')
            
    return render(request,'base/otpverify.html',{'form':form})

def otpgen(request):
    form=pwresetform()
     
    if request.method == "POST":
        
        name=request.POST['username'].lower()
        
        try:
            if User.objects.get(username=name):
                otp=str(random.randint(0,999999))
                
                user=User.objects.get(username=name)
                email=user.email
                try:
                    pro=Profile.objects.get(user_id=user.id)
                    pro.password_token=otp
                    pro.save()
                    
                except:
                    Profile.objects.create(
                    user=user,
                    password_token=otp

                )
                    
                send_mail(
                    subject="your login otp",
                    message= f'( hi your login otp is... {otp} )',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email]
                    )
                messages.error(request,'mail sent')
                return redirect('base:otpverify')
                
        except:
                messages.error(request,'user does not exists')
    return render(request,'base/otpgen.html',{'form':form})







