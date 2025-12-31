from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
import requests

from .models import (
    MentalHealthIssue,
    EmergencyContact,
    Feedback,
    TherapyMusic,
    TherapyImage,
)

def home(request):
    profile = SiteProfile.objects.first()
    return render(request, "home.html", {"profile": profile})

# =========================
# HOME (PUBLIC LANDING PAGE)
# =========================
def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


# =========================
# REGISTER
# =========================
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # ❌ username exists → show error on SAME page
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "auth/register.html")

        # ❌ password mismatch → show error on SAME page
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "auth/register.html")

        # ✅ success
        User.objects.create_user(
            username=username,
            email=email,
            password=password1,
        )

        messages.success(request, "Successfully registered. Please log in.")
        return redirect("login")  # SAME route

    return render(request, "auth/register.html")


# =========================
# LOGIN
# =========================
def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )

        if user:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "auth/login.html")


# =========================
# LOGOUT
# =========================
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("login")


# =========================
# DASHBOARD
# =========================
@login_required
def dashboard(request):
    return render(request, "dashboard.html")


# =========================
# 🎵🖼 THERAPY (MUSIC + IMAGES)
# =========================
@login_required
def therapy(request):
    issues = MentalHealthIssue.objects.all()
    music_list = image_list = None

    if request.method == "POST":
        age = int(request.POST.get("age", 0))
        selected_issues = request.POST.getlist("issues")

        if age < 7:
            messages.error(request, "Therapy is available for age 7 and above.")
            return render(request, "therapy.html", {"issues": issues})

        music_list = (
            TherapyMusic.objects.filter(
                min_age__lte=age,
                max_age__gte=age,
                issues__id__in=selected_issues,
            )
            .distinct()
            .order_by("title")
        )

        image_list = (
            TherapyImage.objects.filter(
                min_age__lte=age,
                max_age__gte=age,
                issues__id__in=selected_issues,
            )
            .distinct()
            .order_by("title")
        )

    return render(
        request,
        "therapy.html",
        {
            "issues": issues,
            "music_list": music_list,
            "image_list": image_list,
        },
    )


# =========================
# AI CHAT (HUGGING FACE – FREE)
# =========================
@login_required
def ai_chat(request):

    # 1️⃣ Load UI
    if request.method == "GET":
        return render(request, "ai_chat.html")

    # 2️⃣ Handle AJAX message
    message = request.POST.get("message", "").strip()
    if not message:
        return JsonResponse({"reply": "Please type something."})

    try:
        response = requests.post(
            "https://router.huggingface.co/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "meta-llama/Meta-Llama-3-8B-Instruct",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a calm, empathetic mental health assistant. "
                            "Only answer mental health related questions. "
                            "Keep answers under 100 words. "
                            "Do not use markdown or bold text."
                        ),
                    },
                    {"role": "user", "content": message},
                ],
                "temperature": 0.7,
                "max_tokens": 200,
            },
            timeout=60,
        )

        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"]

        return JsonResponse({"reply": reply})

    except Exception:
        return JsonResponse(
            {"reply": "AI is temporarily unavailable. Please try again later."}
        )


# =========================
# SOS
# =========================
@login_required
def sos(request):
    contacts = EmergencyContact.objects.all()
    return render(request, "sos.html", {"contacts": contacts})


# =========================
# FEEDBACK
# =========================
@login_required
def feedback(request):
    if request.method == "POST":
        Feedback.objects.create(
            user=request.user,
            rating=request.POST.get("rating"),
            message=request.POST.get("message"),
        )
        messages.success(request, "Thank you for your feedback!")

    return render(request, "feedback.html")


# =========================
# LEGAL PAGES
# =========================
def privacy_policy(request):
    return render(request, "legal/privacy_policy.html")


def terms_of_service(request):
    return render(request, "legal/terms_of_service.html")


def contact(request):
    if request.method == "POST":
        messages.success(
            request,
            "Thank you for contacting us. We’ll get back to you soon.",
        )

    return render(request, "legal/contact.html")
