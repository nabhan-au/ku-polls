from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from django.test.client import RequestFactory
import datetime

from polls.models import Choice, Question, Vote
from polls.views import vote


class VotingTest(TestCase):
    """Test voting function."""

    def setUp(self) -> None:
        """Prepare for test vote function"""
        self.rf = RequestFactory()
        self.login_url = reverse('login')
        self.user_login_data = {
            'username': 'tester1',
            'password': 'test223ss'
        }
        self.user = User.objects.create(username='tester1',
                                        email='test@email.com',
                                        )
        self.user.set_password('test223ss')
        self.user.save()
        self.c = Client()

    def create_question(self, pub_date, end_date, text):
        """Return question model."""
        question = Question.objects.create(question_text=text,
                                           pub_date=pub_date,
                                           end_date=end_date
                                           )
        return question

    def create_choice(self, question, text):
        """Return choice model."""
        choice = Choice.objects.create(question=question,
                                       choice_text=text
                                       )
        return choice

    def test_question_not_selceted(self):
        """Test vote question that not selected choice"""
        question = self.create_question(timezone.now(
        ) + datetime.timedelta(days=0), timezone.now() + datetime.timedelta(days=30), 'q1')
        self.c.post(self.login_url, self.user_login_data)
        url = reverse('polls:vote', args=[question.id])
        response = self.c.post(url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('polls/detail.html')

    def test_question_selected_first_vote(self):
        """Test vote function first time"""
        question = self.create_question(timezone.now(
        ) + datetime.timedelta(days=0), timezone.now() + datetime.timedelta(days=30), 'q1')
        choice = self.create_choice(question, "1")
        request = self.rf
        request.POST = {'choice': choice.id}
        request.user = self.user
        vote(self.rf, question.id)
        self.assertEqual(Vote.objects.filter(choice=choice)[
                         0].user.username, self.user_login_data['username'])

    def test_question_selected_second_vote(self):
        """Test vote function second time"""
        question = self.create_question(timezone.now(
        ) + datetime.timedelta(days=0), timezone.now() + datetime.timedelta(days=30), 'q1')
        choice1 = self.create_choice(question, "1")
        choice2 = self.create_choice(question, "2")
        request = self.rf
        request.POST = {'choice': choice1.id}
        request.user = self.user
        vote(self.rf, question.id)
        self.assertEqual(Vote.objects.filter(choice=choice1).count(), 1)
        request.POST = {'choice': choice2.id}
        vote(self.rf, question.id)
        self.assertEqual(Vote.objects.filter(choice=choice2)[
                         0].user.username, self.user_login_data['username'])
        self.assertEqual(Vote.objects.filter(choice=choice1).count(), 0)
