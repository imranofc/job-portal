"""
URL configuration for jobportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from jbportal.views import *
from jobportal import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('post-job/', post_job, name='post_job'),
    path('jobs/', jobs, name='jobs'),
    path('job/<int:id>/', job, name='job'),
    path('employer-dashboard/', employer_dashboard, name='employer_dashboard'),
    path('manage-job/<int:id>/', manage_job, name='manage_job'),
    path('edit-job/<int:id>', edit_job, name='edit_job'),
    path('access-denied', access_denied, name='access_denied'),
    path('logout/', logout, name='logout'),
    path('job/<int:id>/views/', job_views, name='job_views'),
    path('job/<int:id>/applications/', job_applications, name='job_applications'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', reset_password, name='reset_password'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)