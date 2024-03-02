from django.urls import path
from django.contrib import admin
from dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    
]
