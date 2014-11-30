#coding: utf-8

from django.contrib.admin.templatetags.admin_list import result_hidden_fields,\
    result_headers, items_for_result, ResultList
from django.template import Library
from django.conf import settings


register = Library()


@register.inclusion_tag("admin/django_settings/setting/results.html")
def settings_list(cl):
    """
    Displays the headers and data list together
    """
    from django_settings.models import SettingSet

    headers = list(result_headers(cl))
    num_sorted_fields = 0
    for h in headers:
        if h['sortable'] and h['sorted']:
            num_sorted_fields += 1

    # fake set for settings without setting set
    fake_setting_set_name = 'Unallocated'
    if hasattr(settings, 'DJANGO_SETTINGS_UNALLOCATED_SET'):
        fake_setting_set_name = settings.DJANGO_SETTINGS_UNALLOCATED_SET
    fake_setting_set = SettingSet(pk=0, title=fake_setting_set_name)

    setting_sets = {}
    for setting in cl.result_list:
        setting_set = setting.setting_set or fake_setting_set
        setting_sets.setdefault(setting_set, []) \
                   .append(ResultList(None, items_for_result(cl, setting, None)))


    return {'cl': cl,
            'result_hidden_fields': list(result_hidden_fields(cl)),
            'result_headers': headers,
            'num_sorted_fields': num_sorted_fields,
            'results': setting_sets}
