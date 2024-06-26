"""
URL configuration for job_board_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from job_board.views import signup, login, JobListCreateAPIView, JobRetrieveUpdateDestroyAPIView, AllJobListAPIView, \
    UserJobListAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/signup/', signup, name='signup'),
    path('api/login/', login, name='login'),
    path('api/jobs/all/', AllJobListAPIView.as_view(), name='all-job-list'),
    path('api/jobs/user/', UserJobListAPIView.as_view(), name='user-job-list'),
    path('api/jobs/', JobListCreateAPIView.as_view(), name='job-list-create'),
    path('api/jobs/<int:pk>/', JobRetrieveUpdateDestroyAPIView.as_view(), name='job-detail'),
]
