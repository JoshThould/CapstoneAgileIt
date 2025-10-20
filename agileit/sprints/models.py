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
    
    # Story Model
class Story(models.Model):
    """A user-owned task or feature within a sprint."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="To Do")
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=True, blank=True, related_name="stories")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} [{self.status}]"

    def get_absolute_url(self):
        return reverse("stories:story-detail", kwargs={"pk": self.pk})