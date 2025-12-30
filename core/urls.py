from django.urls import path
from . import views

urlpatterns = [
    # PUBLIC
    path("privacy_policy/", views.privacy_policy, name="privacy_policy"),
    path("terms_of_service/", views.terms_of_service, name="terms_of_service"),
    path("contact/", views.contact, name="contact"),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    # DASHBOARD TABS
    path("dashboard/", views.dashboard, name="dashboard"),
    path("therapy/", views.therapy, name="therapy"),
    path("ai/", views.ai_chat, name="ai"),
    path("sos/", views.sos, name="sos"),
    path("feedback/", views.feedback, name="feedback"),
]
