from django.urls import path, include
from django.contrib import admin

from app.views import page_404

urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls)
]

handler404 = page_404
