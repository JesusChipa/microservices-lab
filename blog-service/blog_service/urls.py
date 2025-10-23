from django.contrib import admin
from django.urls import path, include
from core.views import healthz

urlpatterns = [
    path('admin/', admin.site.urls),
    path('healthz', healthz, name='healthz'),
    path('api/', include('categories.urls')),
    path('api/', include('posts.urls')),
]
