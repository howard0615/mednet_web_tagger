from django.contrib import admin

from .models import Question, Summarization
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['qQuestion_ID', 'sQuestion_Type', 'sQuestion_Filter']
    list_filter = ('sQuestion_Type', 'sQuestion_Filter')
    search_fields = ['qQuestion_ID',]
    ordering = ["-qQuestion_ID"]

class SummarizationAdmin(admin.ModelAdmin):
    list_display = ['question','sUser']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Summarization, SummarizationAdmin)
