from django.contrib import admin
from .models import (
    MentalHealthIssue,
    TherapyMusic,
    TherapyImage,
    EmergencyContact,
    Feedback,
SiteProfile,
)


# =========================
# MENTAL HEALTH ISSUES
# =========================
@admin.register(MentalHealthIssue)
class MentalHealthIssueAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

# core/admin.py
admin.site.register(SiteProfile)

# =========================
# MUSIC THERAPY
# =========================
@admin.register(TherapyMusic)
class TherapyMusicAdmin(admin.ModelAdmin):
    list_display = ("title", "min_age", "max_age")
    list_filter = ("issues",)
    search_fields = ("title",)
    filter_horizontal = ("issues",)


# =========================
# IMAGE THERAPY
# =========================
@admin.register(TherapyImage)
class TherapyImageAdmin(admin.ModelAdmin):
    list_display = ("title", "min_age", "max_age")
    list_filter = ("issues",)
    search_fields = ("title",)
    filter_horizontal = ("issues",)


# =========================
# EMERGENCY CONTACTS
# =========================
@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ("name", "phone")
    search_fields = ("name", "phone")


# =========================
# USER FEEDBACK
# =========================
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("user", "rating")
    list_filter = ("rating",)
    search_fields = ("user__username", "message")
