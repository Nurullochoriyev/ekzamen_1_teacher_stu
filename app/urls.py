from .views.teacher_views import *
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('teacherapi/',Teacher_api.as_view())
]
