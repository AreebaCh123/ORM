from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import StudentViewSet

router = DefaultRouter()
router.register('student', StudentViewSet, basename='student')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    
]
