from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *

# Register your models here.
admin.site.site_header = "StudentMy"
admin.site.site_title  = "StudentMy"
admin.site.index_title = "Administration"

admin.site.register(Content)
admin.site.unregister(Group)
#admin.site.unregister(User)
