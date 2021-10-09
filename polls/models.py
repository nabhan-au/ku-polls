"""This file contain model object in poll application."""
import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    """This class contain model for question."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date', null=True)

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        """Return true published more than 1 days other return false.

        Returns:
            bool: return true is published recently
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Return true if question already published.

        Returns:
            bool: return true if question already published.
        """
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Return true when question can vote other return false.

        Returns:
            bool: return true if question can vote.
        """
        now = timezone.now()
        if self.is_published() and now < self.end_date:
            return True
        return False

    def __str__(self):
        """Retrun question text."""
        return self.question_text


class Choice(models.Model):
    """This class contains choice model."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return choice text."""
        return self.choice_text
