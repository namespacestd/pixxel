from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core import management
from datetime import date
from .models import *

import logging

logger = logging.getLogger('root.' + __name__)

class AppInitialization():

    @staticmethod
    def initialize_database():
        # Initialization code.  This will be run once and only once after all 
        # the models above are loaded.  It makes sure all testing data is loaded in.
        logger.info('Initializing database...')

        # Creates the database if none exists
        management.call_command('syncdb', interactive=False)

        # Load testing data
        if settings.AUTOLOAD_TESTING_DATA:
            if not User.objects.count():
                logger.info('Loading initial data since AUTOLOAD_TESTING_DATA is set to true...')
                
        # Ensure super user exists.
        if settings.AUTOLOAD_ADMIN_ACCOUNT:
            su = User.objects.filter(username='ase1')
            if not su:
                # Ensure that default super-user exists. This check is placed here because
                # it affects performance the least here, and it's the first time the superuser
                # credentials could matter.
                logger.info('Creating initial superuser since AUTOLOAD_ADMIN_ACCOUNT is set to true...')
                su = UserAccount.create_new_user('devfest', '', 'password123')
                su.user.is_superuser = True
                su.user.save()

