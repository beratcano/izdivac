from django.contrib import admin
from .models import AnalyzableData, Question, Answer, UserSession
import csv
from django.http import HttpResponse

class AnalyzableDataInline(admin.StackedInline):
    model = AnalyzableData
    can_delete = False
    verbose_name_plural = 'Analyzable Data'

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    fields = ('question', 'answer_text', 'selected_choice', 'selected_choices')
    readonly_fields = ('question', 'answer_text', 'selected_choice', 'selected_choices')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

class UserSessionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline, AnalyzableDataInline]
    list_display = ('name_surname', 'contact', 'created_at', 'completed')
    list_filter = ('created_at', 'completed')
    search_fields = ('nickname', 'contact_info')
    readonly_fields = ('session_key', 'created_at', 'matching_code')
    actions = ["export_as_csv"]

    def name_surname(self, obj):
        answer = Answer.objects.filter(session=obj, question__text__iexact="İsim Soyisim").order_by('-pk').first()
        if answer:
            return answer.answer_text
        return obj.nickname # Fallback to the original nickname if no specific answer is found
    name_surname.short_description = 'Name Surname'

    def contact(self, obj):
        return obj.contact_info
    contact.short_description = 'Contact Info'

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)

        writer = csv.writer(response)

        questions = Question.objects.all().order_by('section', 'pk')
        header_row = ['Nickname', 'Contact Info'] + [q.text for q in questions]
        writer.writerow(header_row)

        for obj in queryset:
            row = [obj.nickname, obj.contact_info]
            answers = {ans.question_id: ans for ans in obj.answer_set.all()}
            for q in questions:
                answer = answers.get(q.pk)
                if answer:
                    if answer.question.q_type == 'multiple_choice_multiple':
                        row.append(", ".join([c.text for c in answer.selected_choices.all()]))
                    elif answer.selected_choice:
                        row.append(answer.selected_choice.text)
                    else:
                        row.append(answer.answer_text)
                else:
                    row.append("")
            writer.writerow(row)

        return response

    export_as_csv.short_description = "Export Selected to CSV"

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'session', 'answer_text_short')
    list_filter = ('question',)
    search_fields = ('session__nickname', 'session__contact_info', 'answer_text')
    list_select_related = ('session', 'question')

    def answer_text_short(self, obj):
        return (obj.answer_text[:75] + '...') if obj.answer_text and len(obj.answer_text) > 75 else obj.answer_text
    answer_text_short.short_description = 'Answer Text'

@admin.register(AnalyzableData)
class AnalyzableDataAdmin(admin.ModelAdmin):
    list_display = ('session', 'age_min', 'age_max', 'height_min', 'height_max', 'romance_score', 'extroversion_score', 'libido_score')
    search_fields = ('session__nickname',)
    list_filter = ('romance_score', 'extroversion_score', 'libido_score')

admin.site.register(Question)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(UserSession, UserSessionAdmin)
