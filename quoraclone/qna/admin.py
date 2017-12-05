from django.contrib import admin
from qna.models import *

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Upvote)