# core/views.py
from datetime import date, timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .models import Company, ServiceRequest, Task
from .forms import CompanyForm, ServiceRequestForm, TaskForm

def index(request):
    return render(request, "core/index.html")

def companies_list(request):
    companies = Company.objects.select_related("sponsor").all().order_by("name")
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("companies_list")
    else:
        form = CompanyForm()
    return render(request, "core/companies_list.html", {"companies": companies, "form": form})

def requests_list(request):
    qs = ServiceRequest.objects.select_related("company","service_type").all().order_by("-created_at")
    if request.method == "POST":
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("requests_list")
    else:
        form = ServiceRequestForm()
    return render(request, "core/requests_list.html", {"requests": qs, "form": form})

def tasks_list(request):
    tasks = Task.objects.select_related("service_request","assigned_to").all().order_by("due_date")

    status_filter = request.GET.get("status")
    assigned_to_filter = request.GET.get("assigned_to")
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if assigned_to_filter:
        tasks = tasks.filter(assigned_to__username=assigned_to_filter)

    assigned_users = User.objects.filter(task__isnull=False).distinct()

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tasks_list")
    else:
        form = TaskForm()

    return render(request, "core/tasks_list.html", {
        "tasks": tasks,
        "form": form,
        "status_filter": status_filter,
        "assigned_to_filter": assigned_to_filter,
        "assigned_users": assigned_users,
    })

def task_dashboard(request):
    from datetime import date, timedelta
    total_tasks = Task.objects.count()
    not_started = Task.objects.filter(status="not_started").count()
    in_progress = Task.objects.filter(status="in_progress").count()
    completed = Task.objects.filter(status="completed").count()

    today = date.today()
    upcoming_tasks = Task.objects.filter(due_date__range=[today, today + timedelta(days=7)])

    # Optional: upcoming expiries if you added fields on Company
    from .models import Company
    expiring_items = Company.objects.filter(
        trade_license_expiry__range=[today, today + timedelta(days=30)]
    ) | Company.objects.filter(
        establishment_card_expiry__range=[today, today + timedelta(days=30)]
    )

    return render(request, "core/task_dashboard.html", {
        "total_tasks": total_tasks,
        "not_started": not_started,
        "in_progress": in_progress,
        "completed": completed,
        "upcoming_tasks": upcoming_tasks,
        "expiring_items": expiring_items.distinct(),
    })
