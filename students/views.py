from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm, CSVUploadForm
from .models import User, USA_COUNTIES, Opportunity
import csv
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import JsonResponse


import logging

logger = logging.getLogger(__name__)


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
            logger.debug(f"Attempting to authenticate user: {username}")
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("profile")
            else:
                logger.debug("Invalid username or password")
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
    users = User.objects.all()
    return render(request, "students/home.html", {"users": users})


def search_users(request):
    query = request.GET.get("search")
    location = request.GET.get("location")
    experience = request.GET.get("experience")
    results = User.objects.all()

    if query:
        results = results.filter(username__icontains=query)
    if location:
        results = results.filter(county__icontains=location)
    if experience:
        results = results.filter(experience__gte=experience)

    return render(request, "students/search.html", {"results": results})


@login_required
def upload_csv(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES["file"]
            fs = FileSystemStorage()
            filename = fs.save(csv_file.name, csv_file)
            with open(fs.path(filename), newline="") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) != 3:
                        continue
                    county_code, county_name, state = row
                    if (county_code, county_name, state) not in USA_COUNTIES:
                        USA_COUNTIES.append((county_code, county_name, state))
            return redirect("profile")
    else:
        form = CSVUploadForm()
    return render(request, "students/upload_csv.html", {"form": form})


@login_required
def connect_user(request, user_id):
    if request.method == "POST":
        user_to_connect = get_object_or_404(User, id=user_id)
        if user_to_connect != request.user:
            if user_to_connect in request.user.connected_users.all():
                request.user.connected_users.remove(user_to_connect)
                connected = False
            else:
                request.user.connected_users.add(user_to_connect)
                connected = True
            request.user.save()
            return JsonResponse({"connected": connected})
        return JsonResponse({"error": "Cannot connect to yourself"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=400)


@login_required
def opportunities(request):
    opportunities = Opportunity.objects.all()
    for opp in opportunities:
        opp.tags_list = opp.tags.split(",")
    return render(
        request, "students/opportunities.html", {"opportunities": opportunities}
    )


@login_required
def save_opportunity(request, opp_id):
    if request.method == "POST":
        opportunity = get_object_or_404(Opportunity, id=opp_id)
        if request.user in opportunity.saved_by.all():
            opportunity.saved_by.remove(request.user)
            saved = False
        else:
            opportunity.saved_by.add(request.user)
            saved = True
        return JsonResponse({"saved": saved})
    return JsonResponse({"error": "Invalid request method"}, status=400)


@login_required
def apply_opportunity(request, opp_id):
    if request.method == "POST":
        opportunity = get_object_or_404(Opportunity, id=opp_id)
        opportunity.applied_by.add(request.user)
        return JsonResponse({"applied": True})
    return JsonResponse({"error": "Invalid request method"}, status=400)
