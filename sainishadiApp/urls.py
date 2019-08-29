from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('contact/',views.contact,name='contact'),
    path('edit/',views.edit,name='edit'),
    path('send_otp/',views.send_otp,name='send_otp'),
    path('verify/',views.otp_verification,name='verify'),
    path('detail/<int:id>',views.detail,name='detail'),
    path('handlerequest/',views.handlerequest,name='handlerequest'),
    path('register/',views.register,name='register'),
    path('search/',views.search,name='search'),
    path('delete/',views.delete,name='delete'),
    path('forget/',views.forget,name='forget'),
]
