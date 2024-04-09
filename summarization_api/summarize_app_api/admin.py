from django.contrib import admin
from .models import Editor, Summary_text, Description, Rating

admin.site.register(Editor)
admin.site.register(Summary_text)
admin.site.register(Description)
admin.site.register(Rating)