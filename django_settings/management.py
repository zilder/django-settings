# -*- coding: utf-8 -*-
from django.db.models import signals
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from django_settings import models


DEFAULT_SETTINGS = getattr(settings, 'DJANGO_SETTINGS', {})


def initialize_data(sender, **kwargs):
    for set_name, set_data in DEFAULT_SETTINGS.items():
        set_title = set_data.get('title', set_name)

        setting_set, _ = models.SettingSet \
                               .objects.get_or_create(name=set_name,
                                                      defaults={'title': set_title})

        for name, data in set_data.get('settings', {}).iteritems():
            # if original settings style (without title)
            if len(data) == 2:
                type_name, value = data
                title = name
            else:
                type_name, value, title = data

            SettingClass = ContentType.objects \
                                      .get(app_label='django_settings',
                                           model=type_name.lower()).model_class()

            if not models.Setting.objects.value_object_exists(name):
                models.Setting.objects.set_value(name, SettingClass, value, title, setting_set)

signals.post_syncdb.connect(initialize_data, sender=models)
