from django.contrib import admin
from django.urls import path
from students.views import register, user_profile, home, login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('profile/', user_profile, name='profile'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home, name='home'), #homepage
]