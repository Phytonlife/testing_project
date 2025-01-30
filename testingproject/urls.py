from django.contrib import admin
from django.urls import path
from baseapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('api/questions/', views.get_questions, name='get_questions'),
    path('api/save-result/', views.save_result, name='save_result'),
]