from django.contrib import admin

from .models import Document

admin.site.site_header="Diary Admin"

admin.site.register(Document)