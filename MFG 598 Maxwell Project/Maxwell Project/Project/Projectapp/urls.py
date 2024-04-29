from django.contrib import admin
from django.urls import path
from Projectapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', views.index, name='index'),
     path('signup', views.signup, name='signup'),
     path('forgotpassword',views.forgotpassword,name='forgotpassword'),
     path('analysis',views.analysis,name='analysis'),
     path('reset',views.reset,name='reset'),
     path('graphs',views.graphs,name="graphs")
]