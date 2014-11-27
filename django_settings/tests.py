# -*- coding: utf-8 -*-
from django.conf import settings
from django.test import TestCase

from django_settings.models import Setting


DJANGO_SETTINGS = settings.DJANGO_SETTINGS


class SettingDefaults(TestCase):
    def test_default_settings(self):
        """
        Test assuemes that following dict is in your settings.py file:

        DJANGO_SETTINGS = {
           'application_limit': ('Integer', 2),
           'admin_email': ('String', 'kuba.janoszek@gmail.com', 'Admin Email'),
           }
        """
        value = Setting.objects.get_value('application_limit')
        self.assertEquals(value, DJANGO_SETTINGS['application_limit'][1])

        obj = Setting.objects.get(name='admin_email')
        self.assertEquals(obj.title, DJANGO_SETTINGS['admin_email'][2])
