from django.contrib import admin

from klausimai_atsakymai.k_a.models import Question, Answer

# Register your models here.

admin.site.register(Question)
admin.site.register(Answer)