"""vkrs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from task import views

from django.contrib.auth import views as auth_views
from django.contrib import auth as auth
    # import logout, login
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('home/', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('logout-then-login/', auth_views.logout_then_login, name='logout_then_login'),
    path('profile-edit/', views.edit, name='edit'),
    path('profile/', views.user_profile, name='profile-user'),
    path('password-change/', views.change_password, name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(),
       name='password_change_done'),
    path('current-task', views.current_tasks, name='current_tasks'),
    path('finished-task', views.finished_tasks, name='finished_tasks'),
    path('add-task', views.add_task, name='add_tasks'),
    path('themes/<int:theme_id>', views.theme, name='theme'),
    path('add-theme', views.add_theme, name='add-theme'),
    path('edit-task/<int:note>', views.edit_task, name='edit-task'),
    path('edit-theme/<int:theme_id>', views.edit_theme, name='edit-theme'),
    path('tabletask', views.table_tasks, name='table-task'),
    path('task/<int:task_id>', views.task, name='task'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

