from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Sprint, Story

class SprintModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='josh', password='testpass')
        self.sprint = Sprint.objects.create(
            title='Test Sprint',
            owner=self.user,
            start_date='2025-10-01',
            end_date='2025-10-15'
        )

    def test_sprint_str(self):
        self.assertEqual(str(self.sprint), "Sprint: Test Sprint (2025-10-01 to 2025-10-15)")

    def test_get_absolute_url(self):
        url = self.sprint.get_absolute_url()
        self.assertTrue(url.startswith('/'))

class StoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='josh', password='testpass')
        self.sprint = Sprint.objects.create(title='Sprint A', owner=self.user, start_date='2025-10-01', end_date='2025-10-15')
        self.story = Story.objects.create(
            title='Test Story',
            description='A test story',
            status='To Do',
            sprint=self.sprint,
            owner=self.user
        )

    def test_story_str(self):
        self.assertEqual(str(self.story), "Test Story [To Do]")

    def test_story_status_default(self):
        self.assertEqual(self.story.status, 'To Do')

class ViewAccessTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='josh', password='testpass')
        self.other_user = User.objects.create_user(username='notjosh', password='testpass')
        self.sprint = Sprint.objects.create(title='Sprint A', owner=self.user, start_date='2025-10-01', end_date='2025-10-15')

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('sprints:dashboard'))
        self.assertRedirects(response, '/accounts/login/?next=/dashboard/')

    def test_sprint_detail_owner_access(self):
        self.client.login(username='josh', password='testpass')
        response = self.client.get(reverse('sprints:sprint-detail', kwargs={'pk': self.sprint.pk}))
        self.assertEqual(response.status_code, 200)

    def test_sprint_detail_blocked_for_other_user(self):
        self.client.login(username='notjosh', password='testpass')
        response = self.client.get(reverse('sprints:sprint-detail', kwargs={'pk': self.sprint.pk}))
        self.assertRedirects(response, reverse('sprints:sprint-list'))