import uuid
from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.conf import settings


class KeyDoesNotMatchException(Exception):
    pass


class KeyMaxUseExceeded(Exception):
    pass


class RotatingProvisionKey(models.Model):
    """ This model acts as the key which is associated with another model.
     It is a rotating key, i.e. it will expire and generate a new key on a regular interval
     through the help of a scheduling service. """

    key = models.UUIDField(unique=True, default=uuid.uuid4)
    issue_date = models.DateTimeField(blank=True, null=True)
    rotation_date = models.DateTimeField(blank=True, null=True)
    rotation_period = models.DurationField(default=timedelta)
    current_use_count = models.PositiveIntegerField(default=0)
    total_use_count = models.PositiveIntegerField(default=0)
    current_use_max = models.PositiveIntegerField(default=settings.AUP_CURRENT_USE_MAX)

    def __str__(self):
        return "Rotating Provision Key " + str(self.pk)

    def _increment_counts(self):
        self.total_use_count += 1
        self.current_use_count += 1
        return

    def save(self, *args, **kwargs):
        if not self.id:
            # When created for the first time, initialise the issue date:
            self.issue_date = timezone.now()
        self.rotation_period = timedelta(days=settings.AUP_ROTATION_EXPIRY_DAYS,
                                         hours=settings.AUP_ROTATION_EXPIRY_HOURS,
                                         minutes=settings.AUP_ROTATION_EXPIRY_MINUTES)
        self.rotation_date = self.issue_date + self.rotation_period
        self.current_use_max = settings.AUP_CURRENT_USE_MAX
        super(RotatingProvisionKey, self).save(*args, **kwargs)

    def register_use(self):

        """ Attempts to register a use for the provided key.
         Will raise an exception if it is not successful. """

        if self.current_use_count >= self.current_use_max > 0:
            raise KeyMaxUseExceeded("The key has reached it's maximum use count.")
        else:
            self._increment_counts()
            self.save()
            return True

    def rotate_key(self):

        """ Rotate the key, reset the count and update the rotation period. """

        if timezone.now() > self.rotation_date:
            self.key = uuid.uuid4()
            self.issue_date = timezone.now()
            self.rotation_date = self.issue_date + self.rotation_period
            self.current_use_count = 0
            self.save()
            return self.key
