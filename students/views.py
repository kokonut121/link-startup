from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm, CSVUploadForm
from .models import User, USA_COUNTIES
import csv
from django.core.files.storage import FileSystemStorage
from django.db.models import Q


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("profile")
    else:
        form = UserRegisterForm()
    return render(request, "students/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("profile")
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = UserLoginForm()
    return render(request, "students/login.html", {"form": form})


@login_required
def logout_view(request):
    auth_logout(request)
    return render(request, "students/logged_out.html")


@login_required
def user_profile(request):
    return render(request, "students/profile.html", {"user": request.user})


def home(request):
    return render(request, "students/home.html")


def search_users(request):
    query = request.GET.get('search')
    location = request.GET.get('location')
    experience = request.GET.get('experience')
    results = User.objects.all()

    if query:
        results = results.filter(username__icontains=query)
    if location:
        results = results.filter(county__icontains=location)
    if experience:
        results = results.filter(experience__gte=experience)

    return render(request, 'students/search.html', {'results': results})


@login_required
def upload_csv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(csv_file.name, csv_file)
            with open(fs.path(filename), newline='') as f:
                reader = csv.reader(f)
                for row in reader:
                    county_code, county_name = row
                    USA_COUNTIES.append((county_code, county_name))
            return redirect('profile')
    else:
        form = CSVUploadForm()
    return render(request, 'students/upload_csv.html', {'form': form})