from django.contrib import admin
from .models import (
    MentalHealthIssue,
    TherapyMusic,
    TherapyImage,
    EmergencyContact,
    Feedback,
)


# =========================
# MENTAL HEALTH ISSUES
# =========================
@admin.register(MentalHealthIssue)
class MentalHealthIssueAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


# =========================
# 🎵 MUSIC THERAPY
# =========================
@admin.register(TherapyMusic)
class TherapyMusicAdmin(admin.ModelAdmin):
    list_display = ("title", "min_age", "max_age")
    list_filter = ("issues", "min_age", "max_age")
    search_fields = ("title",)
    filter_horizontal = ("issues",)

    fieldsets = (
        ("Basic Info", {"fields": ("title", "audio")}),
        ("Age Group", {"fields": ("min_age", "max_age")}),
        ("Mental Health Issues", {"fields": ("issues",)}),
        (
            "Optional",
            {
                "fields": ("duration",),
            },
        ),
    )


# =========================
# 🖼 IMAGE THERAPY
# =========================
@admin.register(TherapyImage)
class TherapyImageAdmin(admin.ModelAdmin):
    list_display = ("title", "min_age", "max_age")
    list_filter = ("issues", "min_age", "max_age")
    search_fields = ("title",)
    filter_horizontal = ("issues",)

    fieldsets = (
        ("Basic Info", {"fields": ("title", "image")}),
        ("Age Group", {"fields": ("min_age", "max_age")}),
        ("Mental Health Issues", {"fields": ("issues",)}),
        (
            "Optional",
            {
                "fields": ("description",),
            },
        ),
    )


# =========================
# 🚨 EMERGENCY CONTACTS
# =========================
@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ("name", "phone")
    search_fields = ("name", "phone")


# =========================
# ⭐ USER FEEDBACK
# =========================
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("user", "rating")
    list_filter = ("rating",)
    search_fields = ("user__username", "message")
