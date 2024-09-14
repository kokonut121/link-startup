from django.contrib import admin
from django.urls import path
from students.views import (
    register,
    user_profile,
    home,
    login_view,
    logout_view,
    search_users,
    upload_csv,
)

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", user_profile, name="profile"),
    path("search/", search_users, name="search"),
    path("upload-csv/", upload_csv, name="upload_csv"),
    path("admin/", admin.site.urls),
]
