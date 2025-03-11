from django import forms
from .models import Question, Answer, Choice, UserSession
import random
import string
from django.core.exceptions import ValidationError

def generate_matching_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

class AnswerForm(forms.ModelForm):
    nickname = forms.CharField(max_length=100,
                           widget=forms.TextInput(attrs={"class": "form-control"}),
                           label="Your Nickname",
                           required=False)
    contact_info = forms.CharField(max_length=255,
                               widget=forms.TextInput(attrs={"class": "form-control"}),
                               label="Contact Info (Instagram/Email)",
                               required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        question = kwargs.pop("question")
        super().__init__(*args, **kwargs)
        
        # If we have a session, remove nickname and contact_info from required fields
        if self.request and self.request.session.session_key:
            self.fields['nickname'].required = False
            self.fields['contact_info'].required = False
        else:
            self.fields['nickname'].required = True
            self.fields['contact_info'].required = True
        
        field_name = f"question_{question.q_id}"

        if question.q_type == 'open_ended':
            self.fields[field_name] = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}),
                                                      label=question.text)

        elif question.q_type == 'multiple_choice_single':
            choices = [(choice.c_id, choice.text) for choice in question.choices.all()]
            self.fields[field_name] = forms.ChoiceField(choices=choices,
                                                        widget=forms.RadioSelect,
                                                        label=question.text)

        elif question.q_type == 'multiple_choice_multiple':
            choices = [(choice.c_id, choice.text) for choice in question.choices.all()]
            self.fields[field_name] = forms.MultipleChoiceField(choices=choices,
                                                                widget=forms.CheckboxSelectMultiple,
                                                                label=question.text)

    class Meta:
        model = Answer
        fields = ["nickname", "contact_info"]  # We'll add question fields dynamically

    def save(self, commit=True, request=None):
        if request is None:
            raise ValidationError("Request object is required to save the form")

        try:
            # Create or get UserSession first
            if not hasattr(request, 'session') or not request.session.session_key:
                request.session.create()
            
            session, created = UserSession.objects.get_or_create(
                session_key=request.session.session_key,
                defaults={
                    'nickname': self.cleaned_data['nickname'],
                    'contact_info': self.cleaned_data['contact_info'],
                    'matching_code': generate_matching_code()
                }
            )
            
            if not created:
                session.nickname = self.cleaned_data['nickname']
                session.contact_info = self.cleaned_data['contact_info']
                session.save()

            # Create Answer instance
            instance = super().save(commit=False)
            instance.session = session
            
            # Get question information
            question_field = next(name for name in self.fields if name.startswith('question_'))
            question_id = int(question_field.split('_')[1])
            question_instance = Question.objects.get(q_id=question_id)
            instance.question = question_instance

            # Save the instance first to get the primary key
            instance.save()
            
            # Now handle the specific question type
            if question_instance.q_type == "open_ended":
                instance.answer_text = self.cleaned_data.get(question_field)
                instance.selected_choice = None
                instance.selected_choices.clear()
            
            elif question_instance.q_type == "multiple_choice_single":
                choice_id = self.cleaned_data.get(question_field)
                if choice_id:
                    choice_instance = Choice.objects.get(c_id=choice_id)
                    instance.selected_choice = choice_instance
                    instance.selected_choices.clear()
                else:
                    instance.selected_choice = None
                    instance.selected_choices.clear()
            
            elif question_instance.q_type == 'multiple_choice_multiple':
                choice_ids = self.cleaned_data.get(question_field)
                instance.selected_choice = None
                if choice_ids:
                    choice_instances = Choice.objects.filter(c_id__in=choice_ids)
                    instance.selected_choices.set(choice_instances)
                else:
                    instance.selected_choices.clear()
            
            # Save again to persist any changes
            instance.save()
            return instance
            
        except Exception as e:
            raise ValidationError(f"Error saving form: {str(e)}")