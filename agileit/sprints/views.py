from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Sprint, Story, STATUS_CHOICES
from django.contrib import messages
from django.shortcuts import get_object_or_404
# Drag and drop functionality
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json