
import logging
import subprocess
import time

from django.core.management.base import BaseCommand

from auto_user_provision.models import RotatingProvisionKey
from website.models import Device, Status

"""This management command is built to be run by a cron job on at least a 1 hour interval"""


# logger = logging.getLogger("device_connectivity")


class Command(BaseCommand):
    help = 'Rotates keys as required.'

    @staticmethod
    def handle(*args, **options):
        keys = RotatingProvisionKey.objects.all()
        for key in keys:
            key.rotate_key()

