from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# =========================
# MENTAL HEALTH CATEGORY
# =========================
class MentalHealthIssue(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# =========================
# MUSIC THERAPY (CLOUDINARY)
# =========================
class TherapyMusic(models.Model):
    title = models.CharField(max_length=200)
    audio = CloudinaryField(
        resource_type="video",  # audio is treated as video by Cloudinary
        folder="therapy/music",
    )
    min_age = models.PositiveIntegerField(default=7)
    max_age = models.PositiveIntegerField()
    issues = models.ManyToManyField(MentalHealthIssue, related_name="music")
    duration = models.PositiveIntegerField(
        help_text="Duration in seconds", blank=True, null=True
    )

    def __str__(self):
        return self.title


# =========================
# IMAGE THERAPY (CLOUDINARY)
# =========================
class TherapyImage(models.Model):
    title = models.CharField(max_length=200)
    image = CloudinaryField(
        "image",
        folder="therapy/images",
    )
    min_age = models.PositiveIntegerField(default=7)
    max_age = models.PositiveIntegerField()
    issues = models.ManyToManyField(MentalHealthIssue, related_name="images")
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
