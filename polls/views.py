"""This file contain view of each page."""
import logging
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Choice, Question, Vote

logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    """This class contain function and attributes for index page."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions.

        Returns:
            Manager: query set of questions
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """This class contain function and attributes for detail page."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Return set of questions.

        Returns:
            Manager: query set of questions
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """This class contain function and attributes for result page."""

    model = Question
    template_name = 'polls/results.html'


@login_required(login_url='/accounts/login/')
def vote(request, question_id):
    """Plus 1 vote and return results page of questions.

    Args:
        request (HttpRequest): request
        question_id (int): id of questions

    Returns:
        http : return result pages
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice_id = request.POST['choice']
        selected_choice = question.choice_set.get(pk=choice_id)
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select choice. ",
        })
    else:
        if question.can_vote():
            user = request.user
            vote = get_vote_for_user(user, question)
            if not vote:
                vote = Vote.objects.create(user=user, choice=selected_choice)
            else:
                vote[0].choice = selected_choice
                vote[0].save()
            logger.info(
                f'{user.username} voted for question {question_id} for choice {selected_choice.id} at {datetime.now()}'
            )
            return HttpResponseRedirect(reverse('polls:results',
                                        args=(question.id,)))
        else:
            messages.error(request, 'Vote are not available')
            return HttpResponseRedirect(reverse('polls:index'))


def get_vote_for_user(user, poll_question):
    """Find and return an existing vote for a user on a poll question

    Return:
        The user's Vote or None of no vote for this poll_question
    """
    try:
        votes = Vote.objects.filter(user=user).filter(
            choice__question=poll_question)
    except:
        votes = None
    return votes
