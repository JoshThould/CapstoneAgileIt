from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Status Choices
STATUS_CHOICES = [
    ("To Do", "To Do"),
    ("In Progress", "In Progress"),
    ("Done", "Done"),
]

# Sprint Model
class Sprint(models.Model):
    """A time-boxed period for completing a set of stories."""
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Sprint: {self.title} ({self.start_date} to {self.end_date})"

    def get_absolute_url(self):
        return reverse("sprints:sprint-detail", kwargs={"pk": self.pk})