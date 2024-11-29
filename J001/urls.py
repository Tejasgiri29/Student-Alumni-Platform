"""
URL configuration for J001 project.

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
from tone import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/student/', views.student_registration, name='student_registration'),
    path('register/alumni/', views.alumni_registration, name='alumni_registration'),
    path('register/faculty/', views.faculty_registration, name='faculty_registration'),
    path('register/success/', views.success, name='success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('donate/', views.donate, name='donate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
