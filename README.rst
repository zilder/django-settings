django-settings
===============

Simple django reusable application for storing global project settings in database.

By project settings I mean things like admin mail, some default values like default_post_limit etc.
Values are validated depending their type.


API
---

::

  from django_settings import models
  
  # getting values
  models.Setting.objects.get_value('post_limit')
  
  # setting values
  models.Setting.objects.set_value('admin_email', models.String, 'admin@admin.com')

  # you also can set title for setting
  models.Setting.objects.set_value('max_filesize', models.Integer, '1024', 'Max file size')

  # checking if value exists
  models.Setting.objects.value_object_exists('admin_email')



There is ability to setup some defaults via project settings.py file:

::

   DJANGO_SETTINGS = {
      'application_limit': ('Integer', 2),
      'admin_email': ('String', 'admin@mail.com', 'Admin Email'),
   }

   # name of setting set for settings that have no one
   DJANGO_SETTINGS_UNALLOCATED_SET = 'Unallocated'



Settings types 
--------------

Currently there are three setting types supported: Integer, String, PositiveInteger



Admin
-----

Now you can manipulate setting via your admin interface.
Just install the application and put it in your INSTALL_APPS.
