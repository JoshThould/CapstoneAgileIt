from django.urls import path
from .views import (
    DashboardView,
    SprintListView,
    SprintCreateView,
    SprintDetailView,
    SprintUpdateView,
    SprintDeleteView,
    SprintKanbanView,
    StoryListView,
    StoryCreateView,
    StoryDetailView,
    StoryUpdateView,
    StoryDeleteView,
    update_status,
)

app_name = "sprints"

urlpatterns = [
    # Dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Sprints
    path('sprints/', SprintListView.as_view(), name='sprint-list'),
    path('sprints/new/', SprintCreateView.as_view(), name='sprint-create'),
    path('sprints/<int:pk>/', SprintDetailView.as_view(), name='sprint-detail'),
    path('sprints/<int:pk>/edit/', SprintUpdateView.as_view(), name='sprint-edit'),
    path('sprints/<int:pk>/delete/', SprintDeleteView.as_view(), name='sprint-delete'),
    path('sprints/<int:pk>/kanban/', SprintKanbanView.as_view(), name='sprint-kanban'),
    path('stories/', StoryListView.as_view(), name='story-list'),
    path('stories/new/', StoryCreateView.as_view(), name='story-create'),
    path('stories/<int:pk>/', StoryDetailView.as_view(), name='story-detail'),
    path('stories/<int:pk>/edit/', StoryUpdateView.as_view(), name='story-edit'),
    path('stories/<int:pk>/delete/', StoryDeleteView.as_view(), name='story-delete'),
    path('update-status/<int:story_id>/', update_status, name='update-status'), # Drag and drop functionality
]