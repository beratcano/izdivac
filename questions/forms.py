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
        self.question = question # Store the question instance
        
        # If we have a session, remove nickname and contact_info from required fields
        if self.request and self.request.session.session_key:
            self.fields['nickname'].required = False
            self.fields['contact_info'].required = False
        else:
            self.fields['nickname'].required = True
            self.fields['contact_info'].required = True
        
        # Dynamically add question fields based on q_type
        if question.q_type == 'open_ended':
            self.fields[f"question_{question.q_id}"] = forms.CharField(
                widget=forms.Textarea(attrs={"class": "form-control"}),
                label=question.text,
                required=False
            )

        elif question.q_type == 'multiple_choice_single':
            choices = [(choice.c_id, choice.text) for choice in question.choices.all()]
            self.fields[f"question_{question.q_id}"] = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect,
                label=question.text,
                required=False
            )

        elif question.q_type == 'multiple_choice_multiple':
            choices = [(choice.c_id, choice.text) for choice in question.choices.all()]
            self.fields[f"question_{question.q_id}"] = forms.MultipleChoiceField(
                choices=choices,
                widget=forms.CheckboxSelectMultiple,
                label=question.text,
                required=False
            )
        
        elif question.q_type == 'datetime':
            self.fields[f"question_{question.q_id}"] = forms.DateTimeField(
                widget=forms.DateTimeInput(attrs={'type': 'datetime-local', "class": "form-control"}),
                label=question.text,
                required=False
            )
        
        elif question.q_type == 'single_choice_other':
            choices = [(choice.c_id, choice.text) for choice in question.choices.all()] + [('other', 'Diğer')]
            self.fields[f"question_{question.q_id}"] = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect,
                label=question.text,
                required=False
            )
            self.fields[f"question_{question.q_id}_other"] = forms.CharField(
                widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Lütfen belirtin"}),
                label="",
                required=False
            )
        
        elif question.q_type == 'multiple_choice_other':
            choices = [(choice.c_id, choice.text) for choice in question.choices.all()] + [('other', 'Diğer')]
            self.fields[f"question_{question.q_id}"] = forms.MultipleChoiceField(
                choices=choices,
                widget=forms.CheckboxSelectMultiple,
                label=question.text,
                required=False
            )
            self.fields[f"question_{question.q_id}_other"] = forms.CharField(
                widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Lütfen belirtin"}),
                label="",
                required=False
            )
        
        elif question.q_type == 'multi_text':
            self.fields[f"question_{question.q_id}_part1"] = forms.CharField(
                widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Okul"}),
                label=f"{question.text} (Okul)",
                required=False
            )
            self.fields[f"question_{question.q_id}_part2"] = forms.CharField(
                widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Bölüm"}),
                label=f"{question.text} (Bölüm)",
                required=False
            )
            self.fields[f"question_{question.q_id}_part3"] = forms.CharField(
                widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Yıl"}),
                label=f"{question.text} (Yıl)",
                required=False
            )
        
        elif question.q_type == 'number_range':
            self.fields[f"question_{question.q_id}_min"] = forms.IntegerField(
                widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Min"}),
                label=f"{question.text} (Min)",
                required=False
            )
            self.fields[f"question_{question.q_id}_max"] = forms.IntegerField(
                widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Max"}),
                label=f"{question.text} (Max)",
                required=False
            )
        
        elif question.q_type == 'slider':
            self.fields[f"question_{question.q_id}"] = forms.IntegerField(
                initial=question.min_value,
                widget=forms.NumberInput(attrs={
                    "class": "form-control slider-input",
                    "type": "range",
                    "min": question.min_value,
                    "max": question.max_value,
                    "oninput": f"document.getElementById('slider_value_{question.q_id}').innerText = this.value"
                }),
                label=question.text,
                required=False
            )

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
            
            session, created_session = UserSession.objects.get_or_create(
                session_key=request.session.session_key,
                defaults={
                    'nickname': self.cleaned_data['nickname'],
                    'contact_info': self.cleaned_data['contact_info'],
                    'matching_code': generate_matching_code()
                }
            )
            
            if not created_session:
                session.nickname = self.cleaned_data['nickname']
                session.contact_info = self.cleaned_data['contact_info']
                session.save()

            # Prepare data for Answer update_or_create
            answer_defaults = {}
            question_field_prefix = f"question_{self.question.q_id}"
            question_instance = self.question

            if question_instance.q_type in ["open_ended", "datetime", "slider"]:
                answer_defaults['answer_text'] = self.cleaned_data.get(question_field_prefix)
                answer_defaults['selected_choice'] = None
            
            elif question_instance.q_type == "multiple_choice_single":
                choice_id = self.cleaned_data.get(question_field_prefix)
                answer_defaults['selected_choice'] = Choice.objects.get(c_id=choice_id) if choice_id else None
                answer_defaults['answer_text'] = None
            
            elif question_instance.q_type == 'single_choice_other':
                selected_value = self.cleaned_data.get(question_field_prefix)
                if selected_value == 'other':
                    answer_defaults['answer_text'] = self.cleaned_data.get(f"{question_field_prefix}_other")
                    answer_defaults['selected_choice'] = None
                elif selected_value:
                    answer_defaults['selected_choice'] = Choice.objects.get(c_id=selected_value)
                    answer_defaults['answer_text'] = None
                else:
                    answer_defaults['selected_choice'] = None
                    answer_defaults['answer_text'] = None
            
            elif question_instance.q_type == 'multi_text':
                part1 = self.cleaned_data.get(f"{question_field_prefix}_part1", '')
                part2 = self.cleaned_data.get(f"{question_field_prefix}_part2", '')
                part3 = self.cleaned_data.get(f"{question_field_prefix}_part3", '')
                answer_defaults['answer_text'] = f"Okul: {part1}, Bölüm: {part2}, Yıl: {part3}"
                answer_defaults['selected_choice'] = None
            
            elif question_instance.q_type == 'number_range':
                min_val = self.cleaned_data.get(f"{question_field_prefix}_min")
                max_val = self.cleaned_data.get(f"{question_field_prefix}_max")
                if min_val is not None and max_val is not None:
                    answer_defaults['answer_text'] = f"{min_val}-{max_val}"
                elif min_val is not None:
                    answer_defaults['answer_text'] = f"{min_val}-"
                elif max_val is not None:
                    answer_defaults['answer_text'] = f"-{max_val}"
                else:
                    answer_defaults['answer_text'] = None
                answer_defaults['selected_choice'] = None
            
            # For multiple_choice_multiple and multiple_choice_other, answer_text and selected_choice are None
            elif question_instance.q_type in ["multiple_choice_multiple", "multiple_choice_other"]:
                answer_defaults['answer_text'] = None
                answer_defaults['selected_choice'] = None

            # Use update_or_create for the Answer instance
            answer_instance, created_answer = Answer.objects.update_or_create(
                session=session,
                question=question_instance,
                defaults=answer_defaults
            )

            # Handle ManyToMany fields separately after answer_instance is created/updated
            if question_instance.q_type in ["multiple_choice_multiple", "multiple_choice_other"]:
                selected_choices_ids = self.cleaned_data.get(question_field_prefix)
                if selected_choices_ids:
                    # Filter out 'other' if it was in selected_choices_ids for multiple_choice_other
                    if question_instance.q_type == "multiple_choice_other" and 'other' in selected_choices_ids:
                        selected_choices_ids.remove('other')
                    choice_instances = Choice.objects.filter(c_id__in=selected_choices_ids)
                    answer_instance.selected_choices.set(choice_instances)
                else:
                    answer_instance.selected_choices.clear()
            
            return answer_instance
            
        except Exception as e:
            raise ValidationError(f"Error saving form: {str(e)}")