"""This file contain model object in poll application."""
import datetime
import logging
from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

logger = logging.getLogger(__name__)


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

    def votes(self):
        """Count vote that user vote in each choice."""
        count = Vote.objects.filter(choice=self).count()
        return count

    def __str__(self):
        """Return choice text."""
        return self.choice_text


class Vote(models.Model):
    """Class contain choice and user that vote that choice"""

    user = models.ForeignKey(
        User, null=False, blank=False, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def vote_str(self):
        """Return string which show choice that user vote."""
        return f"You voted {self.choice.choice_text}"

    def __str__(self) -> str:
        """Return vote text"""
        return f"Vote by {self.user.username} for {self.choice.choice_text}"


def get_client_ip(request):
    """Get client ip adress.

    Returns:
        str: client ip adress
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    """Call after user login and show log info.

    Args:
        user (User): user model
    """
    ip = get_client_ip(request)
    logger.info(f"{user} logged in from ip:{ip} at {datetime.datetime.now()}")


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    """Call after user logout and show log info.

    Args:
        user (User): user model
    """
    ip = get_client_ip(request)
    logger.info(f"{user} logged out with ip:{ip} at {datetime.datetime.now()}")


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    """Call after user login with wrong username and password. And show log warning.

    Args:
        user (User): user model
    """
    logger.warning(
        f'login failed for: {credentials} at {datetime.datetime.now()}')
