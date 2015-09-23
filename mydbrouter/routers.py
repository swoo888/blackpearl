import sys
from django.conf import settings
import random
import logging

logger = logging.getLogger('djangoproject.mydbrouters')
router_enabled = True
slave_choice = None


#noinspection PyUnusedLocal
class MasterSlaveRouter(object):

    def db_for_read(self, model, **hints):
        if settings.TESTING:
            return 'default'
        if model._meta.object_name == 'Session' and \
            'django.contrib' in str(model)[8:]:
            return 'session'
        if model._meta.object_name == 'ReviewPhoto':
            return 'review_photos'
        global router_enabled
        if not router_enabled:
            return 'default'
        if not settings.USE_MULTI_DB:
            return 'default'

        # carry over state if this is related
        try:
            instance = hints['instance']
        except KeyError:
            pass
        else:
            if instance._state.db == 'default':
                return 'default'

        return self._choose_slave()

    def _choose_slave(self):
        global slave_choice
        #return 'default'
        if not slave_choice:
            slave_choice = random_slave()
        return slave_choice

    def db_for_write(self, model, **hints):
        if settings.TESTING:
            return 'default'
        if model._meta.object_name == 'Session' and \
            'django.contrib' in str(model)[8:]:
            return 'session'
        if model._meta.object_name == 'ReviewPhoto':
            return 'review_photos'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_syncdb(self, db, model):
        if settings.TESTING:
            return True
        if db == 'session':
            if str(model._meta) == 'sessions.session':
                return True
            return False
        if db == 'review_photos':
            if str(model._meta) == 'review_photos.review_photo':
                return True
            return False
        if db == 'default':
            if str(model._meta) == 'review_photos.review_photo':
                return False
            return True
        return False


def random_slave():
    return random.choice(
        ['slave',])
