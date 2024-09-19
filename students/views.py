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
                return redirect("home")
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


@login_required
def other_user_profile(request, user_id):
    req_user = get_object_or_404(User, id=user_id)
    return render(request, "students/profile.html", {"user": req_user})


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
def home(request):
    connected_users = request.user.connected_users.all()
    unconnected_users = User.objects.exclude(id__in=connected_users).exclude(
        id=request.user.id
    )
    return render(
        request,
        "students/home.html",
        {"connected_users": connected_users, "unconnected_users": unconnected_users},
    )


@login_required
def search_users(request):
    query = request.GET.get("query", "")
    users = User.objects.filter(
        Q(username__icontains=query)
        | Q(display_name__icontains=query)
        | Q(title__icontains=query)
        | Q(university__icontains=query)
    ).exclude(id=request.user.id)

    users_data = [
        {
            "id": user.id,
            "username": user.username,
            "display_name": user.display_name,
            "title": user.title,
            "university": user.university,
            "num_connections": user.num_connections,
            "avatar": user.avatar.url if user.avatar else None,
            "connected": user in request.user.connected_users.all(),
            "activity": user.activity,
        }
        for user in users
    ]
    return JsonResponse({"users": users_data})


@login_required
def opportunities(request):
    type_filter = request.GET.get("type", "")
    location_filter = request.GET.get("location", "")
    experience_filter = request.GET.get("experience", "")
    tab_filter = request.GET.get("tab", "recent")
    query = request.GET.get("query", "")

    opportunities = Opportunity.objects.all()

    if type_filter:
        opportunities = opportunities.filter(type=type_filter)
    if location_filter:
        opportunities = opportunities.filter(location=location_filter)
    if experience_filter:
        opportunities = opportunities.filter(experience=experience_filter)
    if query:
        opportunities = opportunities.filter(
            Q(title__icontains=query) |
            Q(company__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__icontains=query)
        )
    if tab_filter == "saved":
        opportunities = opportunities.filter(saved_by=request.user)
    elif tab_filter == "applied":
        opportunities = opportunities.filter(applied_by=request.user)

    opportunities_data = [
        {
            "id": opp.id,
            "title": opp.title,
            "company": opp.company,
            "description": opp.description,
            "tags": opp.tags.split(","),
            "type": opp.type,
            "location": opp.location,
            "salary": opp.salary,
            "experience": opp.experience,
            "url": opp.url,
            "saved": request.user in opp.saved_by.all(),
            "applied": request.user in opp.applied_by.all(),
        }
        for opp in opportunities
    ]

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({"opportunities": opportunities_data})

    return render(request, "students/opportunities.html", {"opportunities": opportunities})

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
        if request.user in opportunity.applied_by.all():
            opportunity.applied_by.remove(request.user)
            applied = False
        else:
            opportunity.applied_by.add(request.user)
            applied = True
        return JsonResponse({"applied": applied})
    return JsonResponse({"error": "Invalid request method"}, status=400)


@login_required
def search_opportunities(request):
    query = request.GET.get("query", "")
    opportunities = Opportunity.objects.filter(
        Q(title__icontains=query)
        | Q(company__icontains=query)
        | Q(description__icontains=query)
        | Q(tags__icontains=query)
    )
    opportunities_data = [
        {
            "id": opp.id,
            "title": opp.title,
            "company": opp.company,
            "description": opp.description,
            "tags": opp.tags.split(","),
            "type": opp.type,
            "location": opp.location,
            "salary": opp.salary,
            "experience": opp.experience,
            "url": opp.url,
            "saved": request.user in opp.saved_by.all(),
            "applied": request.user in opp.applied_by.all(),
        }
        for opp in opportunities
    ]
    return JsonResponse({"opportunities": opportunities_data})


