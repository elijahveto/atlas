from django.contrib import admin
from .models import *
from django.conf import settings
import os


class Media:
    js = [settings.TINYMCE_JS_URL,
    os.path.join(settings.STATIC_ROOT, 'grappelli/tinymce_setup/tinymce_setup.js')]


admin.site.register(Post)
admin.site.register(Section)
admin.site.register(Comment)
admin.site.register(Likes)

