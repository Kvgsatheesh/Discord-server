from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView

app_name='base'

urlpatterns = [
    path('',views.home,name='home'),
    path('room/<int:id>',views.room,name='room'),
    path('create-room',views.createroom,name='create-room'),
    path('update-room/<int:id>',views.updateroom,name='update-room'),
    path('delete-room/<int:id>',views.deleteroom,name='delete-room'),
    path('login/',views.loginpageview,name='login'),
    path('logout/',views.logoutpageview,name='logout'),
    path('signup/',views.signup,name='signup'),
    path('addtopic',views.addtopic,name='addtopic'),
    
    path('delete-msg/<int:mid>/<int:rid>',views.deletemessage,name='delete-message'),
    path('adelete-msg/<int:mid>',views.adeletemessage,name='adelete-message'),
    path('profile/<int:id>',views.userprofile,name='profile'),
    path('update-profile',views.updateuser,name='update-profile'),
    path('update-message/<int:id>/<int:rid>',views.updatemessage,name='update-message'),
    path( 'password/',views.PasswordsChangeView.as_view(template_name='base/change-password.html'),name='PasswordChangeView'),
    path('password_success',views.password_success,name='password_success'),
    path('passwordreset/',views.passwordreset,name='passwordreset'),
    path('setpassword/<token>/<int:id>',views.setpassword,name='setpassword'),
    path('otpgen/',views.otpgen,name='otpgen'),
    path('otpverify/',views.otpverify,name='otpverify'),
    
]