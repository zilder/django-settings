# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _


class BaseSetting(models.Model):
    class Meta:
        abstract = True

    def __unicode__(self):
        return u'%s' % self.value


class String(BaseSetting):
    value = models.CharField(max_length=254)


class Integer(BaseSetting):
    value = models.IntegerField()


class PositiveInteger(BaseSetting):
    value = models.PositiveIntegerField()


class SettingManager(models.Manager):
    def get_value(self, name, **kw):
        if 'default' in kw:
            if not self.value_object_exists(name):
                return kw.get('default')
        return self.get(name=name).setting_object.value

    def value_object_exists(self, name):
        queryset = self.filter(name=name)
        return queryset.exists() and queryset[0].setting_object

    def set_value(self, name, SettingClass, value, title=None,
                  setting_set=None):
        setting = Setting(name=name, title=title or name,
                          setting_set=setting_set)

        if self.value_object_exists(name):
            setting = self.get(name=name)
            setting_object = setting.setting_object
            setting_object.delete()

        setting.setting_object = SettingClass.objects \
                                             .create(value=value)
        setting.save()
        return setting


class SettingSet(models.Model):
    class Meta:
        verbose_name = _('Setting set')
        verbose_name_plural = _('Setting sets')

    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return self.title


class Setting(models.Model):
    class Meta:
        verbose_name = _('Setting')
        verbose_name_plural = _('Settings')

    objects = SettingManager()

    setting_type = models.ForeignKey(ContentType)
    setting_id = models.PositiveIntegerField()
    setting_object = generic.GenericForeignKey('setting_type', 'setting_id')

    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    setting_set = models.ForeignKey(SettingSet, related_name='settings', blank=True, null=True)
