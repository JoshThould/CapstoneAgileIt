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



# Dashboard view
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'sprints/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stories_todo'] = Story.objects.filter(status='To Do', owner=self.request.user)
        context['stories_in_progress'] = Story.objects.filter(status='In Progress', owner=self.request.user)
        context['stories_done'] = Story.objects.filter(status='Done', owner=self.request.user)
        return context

# Kanban board view
class SprintKanbanView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'sprints/kanban.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sprint = get_object_or_404(Sprint, pk=self.kwargs['pk'])

        status_list = [status for status, _ in STATUS_CHOICES]  # ✅ Extract status keys

        context['sprint'] = sprint
        context['columns'] = [
            {
                'status': status,
                'stories': sprint.stories.filter(status=status, owner=self.request.user)
            }
            for status in status_list
        ]
        return context

    def test_func(self):
        sprint = get_object_or_404(Sprint, pk=self.kwargs['pk'])
        return sprint.owner == self.request.user

# Sprints Views

class SprintListView(LoginRequiredMixin, ListView):
    model = Sprint
    template_name = 'sprints/sprint_list.html'
    context_object_name = 'sprints'

    def get_queryset(self):
        return Sprint.objects.filter(owner=self.request.user)

class SprintCreateView(LoginRequiredMixin, CreateView):
    model = Sprint
    fields = ['title', 'start_date', 'end_date']  # exclude 'user' from the form
    template_name = 'sprints/sprint_form.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user  # set the owner before saving
        return super().form_valid(form)

class SprintDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Sprint
    template_name = 'sprints/sprint_detail.html'
    context_object_name = 'sprint'

    def test_func(self):
        sprint = self.get_object()
        return sprint.owner == self.request.user
    
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to view this sprint.")
        return redirect('sprints:sprint-list')

class SprintUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Sprint
    fields = ['title', 'start_date', 'end_date']
    template_name = 'sprints/sprint_form.html'
    success_url = reverse_lazy('sprints:sprint-list')

    def test_func(self):
        sprint = self.get_object()
        return sprint.owner == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Sprint updated successfully.")
        return super().form_valid(form)
    
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to view this sprint.")
        return redirect('sprints:sprint-list')

class SprintDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Sprint
    template_name = 'sprints/sprint_confirm_delete.html'
    success_url = reverse_lazy('sprints:sprint-list')

    def test_func(self):
        sprint = self.get_object()
        return sprint.owner == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Sprint deleted successfully.")
        return super().delete(request, *args, **kwargs)
    
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to view this sprint.")
        return redirect('sprints:sprint-list')
    
    # Story Views
class StoryListView(LoginRequiredMixin, ListView):
    model = Story
    template_name = 'sprints/story_list.html'
    context_object_name = 'stories'

    def get_queryset(self):
        return Story.objects.filter(owner=self.request.user)

class StoryCreateView(LoginRequiredMixin, CreateView):
    model = Story
    fields = ['title', 'description', 'status', 'sprint']
    template_name = 'sprints/story_form.html'
    success_url = reverse_lazy('sprints:story-list')

    def get_initial(self):
        sprint_id = self.request.GET.get('sprint')
        if sprint_id:
            try:
                return {'sprint': Sprint.objects.get(pk=sprint_id)}
            except Sprint.DoesNotExist:
                pass
        return super().get_initial()

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Story created successfully.")
        return super().form_valid(form)



class StoryDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Story
    template_name = 'sprints/story_detail.html'
    context_object_name = 'story'

    def test_func(self):
        story = self.get_object()
        return story.owner == self.request.user
    
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to view this sprint.")
        return redirect('sprints:sprint-list')

    
class StoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Story
    fields = ['title', 'description', 'status', 'sprint']
    template_name = 'sprints/story_form.html'
    
    def get_success_url(self):
        return reverse_lazy('sprints:sprint-kanban', kwargs={'pk': self.object.sprint.pk})

    def test_func(self):
        story = self.get_object()
        return story.owner == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Story updated successfully.")
        return super().form_valid(form)
    
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to view this sprint.")
        return redirect('sprints:sprint-list')


class StoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):             
    model = Story
    template_name = 'sprints/story_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('sprints:sprint-kanban', kwargs={'pk': self.object.sprint.pk})

    def test_func(self):
        story = self.get_object()
        return story.owner == self.request.user
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Story deleted successfully.")
        return super().delete(request, *args, **kwargs)
    
    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to view this sprint.")
        return redirect('sprints:sprint-list')

# Drag and drop functionality

@csrf_exempt
def update_status(request, story_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_status = data.get('status')
        story = Story.objects.get(pk=story_id)
        story.status = new_status
        story.save()
        return JsonResponse({'success': True})