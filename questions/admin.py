from django.contrib import admin
from .models import AnalyzableData, Question, Answer, UserSession

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    fields = ('question', 'answer_text', 'selected_choices')
    readonly_fields = ('question', 'answer_text', 'selected_choices')

class UserSessionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('session_key', 'nickname', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('session_key', 'nickname')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('session', 'question', 'answer_text')
    list_filter = ('session', 'question')
    search_fields = ('session__session_key', 'session__nickname')
    list_select_related = ('session', 'question')

@admin.register(AnalyzableData)
class AnalyzableDataAdmin(admin.ModelAdmin):
    list_display = ('session', 'age_min', 'age_max', 'height_min', 'height_max', 'zodiac_sign')
    search_fields = ('session__nickname', 'age_min', 'age_max')
    list_filter = ('age_min', 'age_max', 'zodiac_sign')

admin.site.register(Question)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(UserSession, UserSessionAdmin)
