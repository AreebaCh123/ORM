from django.contrib import admin
from django.urls import path
from app.views import OrmTestView  # Change `app` to your actual app name

urlpatterns = [
    path('admin/', admin.site.urls),
    path('orm-test/', OrmTestView.as_view(), name='orm-test'),
]
