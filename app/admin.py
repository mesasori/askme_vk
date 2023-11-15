from django.contrib import admin
from .models import Question, Tag, Answer, Profile, Like

# Register your models here.
admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Answer)
admin.site.register(Profile)
admin.site.register(Like)
