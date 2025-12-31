from django.db import models
from django.contrib.auth.models import User


# =========================
# MENTAL HEALTH CATEGORY
# =========================
class MentalHealthIssue(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# =========================
# MUSIC THERAPY
# =========================
class TherapyMusic(models.Model):
    title = models.CharField(max_length=200)
    audio = models.FileField(upload_to="therapy_music/")
    min_age = models.IntegerField(default=7)
    max_age = models.IntegerField()
    issues = models.ManyToManyField(MentalHealthIssue)
    duration = models.IntegerField(
        help_text="Duration in seconds", blank=True, null=True
    )

    def __str__(self):
        return self.title


# =========================
# PHOTO THERAPY
# =========================
class TherapyImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="therapy_images/")
    min_age = models.IntegerField(default=7)
    max_age = models.IntegerField()
    issues = models.ManyToManyField(MentalHealthIssue)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

# =========================
# EMERGENCY CONTACTS
# =========================
class EmergencyContact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} - {self.phone}"


# =========================
# USER FEEDBACK
# =========================
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    message = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.rating}/5"
