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
    connect_user,
    opportunities,
    save_opportunity,
    apply_opportunity,
    search_opportunities,
    other_user_profile
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", user_profile, name="profile"),
    path("search/", search_users, name="search"),
    path("upload-csv/", upload_csv, name="upload_csv"),
    path("admin/", admin.site.urls),
    path("connect/<int:user_id>/", connect_user, name="connect_user"),
    path("opportunities/", opportunities, name="opportunities"),
    path('save_opportunity/<int:opp_id>/', save_opportunity, name='save_opportunity'),
    path('apply_opportunity/<int:opp_id>/', apply_opportunity, name='apply_opportunity'),
    path('search_opportunities/', search_opportunities, name='search_opportunities'),
    path('profile/<int:user_id>/', other_user_profile, name="profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)