from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Question, Answer, Choice, UserSession, AnalyzableData
from .forms import AnswerForm
from django.db.transaction import atomic
from django.db.models import Q

def analyze_and_save_data(session):
    answers = Answer.objects.filter(session=session)
    data = {}

    for answer in answers:
        question_text = answer.question.text
        if "Yaş Aralığı" in question_text:
            if answer.answer_text:
                try:
                    age_range = answer.answer_text.split('-')
                    data['age_min'] = int(age_range[0])
                    data['age_max'] = int(age_range[1])
                except (ValueError, IndexError):
                    data['age_min'] = None
                    data['age_max'] = None
            else:
                data['age_min'] = None
                data['age_max'] = None
        elif "Boy Aralığı" in question_text:
            if answer.answer_text:
                try:
                    height_range = answer.answer_text.split('-')
                    data['height_min'] = int(height_range[0])
                    data['height_max'] = int(height_range[1])
                except (ValueError, IndexError):
                    data['height_min'] = None
                    data['height_max'] = None
            else:
                data['height_min'] = None
                data['height_max'] = None
        elif "Romantiklik Seviyesi" in question_text:
            if answer.answer_text:
                try:
                    data['romance_score'] = int(answer.answer_text)
                except ValueError:
                    data['romance_score'] = None
            else:
                data['romance_score'] = None
        elif "Çekicilik Seviyesi" in question_text:
            if answer.answer_text:
                try:
                    data['attraction_score'] = int(answer.answer_text)
                except ValueError:
                    data['attraction_score'] = None
            else:
                data['attraction_score'] = None
        elif "Dışa Dönüklük Seviyesi" in question_text:
            if answer.answer_text:
                try:
                    data['extroversion_score'] = int(answer.answer_text)
                except ValueError:
                    data['extroversion_score'] = None
            else:
                data['extroversion_score'] = None
        elif "Libido Seviyesi" in question_text:
            if answer.answer_text:
                try:
                    data['libido_score'] = int(answer.answer_text)
                except ValueError:
                    data['libido_score'] = None
            else:
                data['libido_score'] = None
        elif "İlişki Durumu" in question_text:
            data['relationship_status'] = answer.answer_text
        elif "Nasıl Bir İlişki Arıyorsunuz" in question_text:
            data['desired_relationship_type'] = ", ".join([c.text for c in answer.selected_choices.all()])

    AnalyzableData.objects.update_or_create(session=session, defaults=data)

    session.completed = True
    session.save()

def welcome(request):
    return render(request, 'welcome.html')

def start_questionnaire(request):
    # Reset any existing session to ensure a fresh start
    session_key = request.session.session_key
    if session_key:
        UserSession.objects.filter(session_key=session_key).delete()
    
    # Create a new session
    request.session.flush()
    request.session.create()

    first_question = Question.objects.order_by('section', 'pk').first()
    if first_question is None:
        return redirect('no_questions')
    
    request.session['current_question_id'] = first_question.pk
    return redirect('submit_answer')

def submit_answer(request):
    current_question_id = request.session.get('current_question_id')
    if current_question_id is None:
        # If no current question in session, redirect to start
        return redirect('start')

    question = get_object_or_404(Question, pk=current_question_id)
    
    if request.method == "POST":
        form = AnswerForm(request.POST, question=question, request=request)
        
        if form.is_valid():
            try:
                with atomic():
                    answer_data = {}
                    question_field_name = f"question_{question.q_id}"

                    if question.q_type in ["open_ended", "datetime", "slider", "multi_text", "number_range"]:
                        answer_data['answer_text'] = form.cleaned_data.get(question_field_name)
                        answer_data['selected_choice'] = None
                    elif question.q_type == "multiple_choice_single":
                        choice_id = form.cleaned_data.get(question_field_name)
                        answer_data['selected_choice'] = Choice.objects.get(c_id=choice_id) if choice_id else None
                        answer_data['answer_text'] = None
                    elif question.q_type == "single_choice_other":
                        selected_value = form.cleaned_data.get(question_field_name)
                        if selected_value == 'other':
                            answer_data['answer_text'] = form.cleaned_data.get(f"{question_field_name}_other")
                            answer_data['selected_choice'] = None
                        else:
                            answer_data['selected_choice'] = Choice.objects.get(c_id=selected_value) if selected_value else None
                            answer_data['answer_text'] = None
                    elif question.q_type == "multiple_choice_multiple":
                        # For ManyToMany, we'll handle it after update_or_create
                        answer_data['answer_text'] = None
                        answer_data['selected_choice'] = None
                    elif question.q_type == "multiple_choice_other":
                        selected_values = form.cleaned_data.get(question_field_name)
                        other_text = form.cleaned_data.get(f"{question_field_name}_other")
                        if 'other' in selected_values and other_text:
                            answer_data['answer_text'] = other_text
                            selected_values.remove('other')
                        else:
                            answer_data['answer_text'] = None
                        # For ManyToMany, we'll handle it after update_or_create
                        answer_data['selected_choice'] = None

                    answer_instance = form.save(commit=False, request=request)
                    session = answer_instance.session

                    # Ensure there's only one answer per session and question
                    existing_answers = Answer.objects.filter(session=session, question=question)
                    if existing_answers.count() > 1:
                        # Keep the most recent one and delete the rest
                        latest_answer = existing_answers.latest('id')
                        existing_answers.exclude(pk=latest_answer.pk).delete()

                    answer, created = Answer.objects.update_or_create(
                        session=session,
                        question=question,
                        defaults=answer_data
                    )
                    answer_instance = answer # Ensure answer_instance refers to the updated/created object

                    # Handle ManyToMany fields after creation/update
                    if question.q_type in ["multiple_choice_multiple", "multiple_choice_other"]:
                        selected_choices_ids = form.cleaned_data.get(question_field_name)
                        if selected_choices_ids:
                            # Filter out 'other' if it was in selected_choices_ids for multiple_choice_other
                            if question.q_type == "multiple_choice_other" and 'other' in selected_choices_ids:
                                selected_choices_ids.remove('other')
                            choice_instances = Choice.objects.filter(c_id__in=selected_choices_ids)
                            answer.selected_choices.set(choice_instances)
                        else:
                            answer.selected_choices.clear()
                    
                    # For multi_text and number_range, the answer_text needs to be formatted
                    if question.q_type == 'multi_text':
                        part1 = form.cleaned_data.get(f"{question_field_name}_part1", '')
                        part2 = form.cleaned_data.get(f"{question_field_name}_part2", '')
                        part3 = form.cleaned_data.get(f"{question_field_name}_part3", '')
                        answer.answer_text = f"Okul: {part1}, Bölüm: {part2}, Yıl: {part3}"
                        answer.save()
                    elif question.q_type == 'number_range':
                        min_val = form.cleaned_data.get(f"{question_field_name}_min")
                        max_val = form.cleaned_data.get(f"{question_field_name}_max")
                        if min_val is not None and max_val is not None:
                            answer.answer_text = f"{min_val}-{max_val}"
                        elif min_val is not None:
                            answer.answer_text = f"{min_val}-"
                        elif max_val is not None:
                            answer.answer_text = f"-{max_val}"
                        else:
                            answer.answer_text = None
                        answer.save()

                next_question = Question.objects.filter(section=question.section,
                                                        pk__gt=question.pk).order_by("pk").first()
                
                if next_question:
                    request.session['current_question_id'] = next_question.pk
                    return redirect("submit_answer")
                else:
                    next_section_question = Question.objects.filter(
                        section__gt=question.section
                    ).order_by("section","pk").first()
                    
                    if next_section_question:
                        request.session['current_question_id'] = next_section_question.pk
                        return redirect("submit_answer")
                    else:
                        # All questions answered, now analyze
                        session = UserSession.objects.get(session_key=request.session.session_key)
                        analyze_and_save_data(session)
                        return redirect("success")
            except Exception as e:
                print("Error saving form:", str(e))  # Debug print
                raise
    else:
        # For GET requests, load existing answer if available
        session_key = request.session.session_key
        if session_key:
            try:
                session = UserSession.objects.get(session_key=session_key)
                existing_answer = Answer.objects.filter(session=session, question=question).first()
                if existing_answer:
                    # Populate form with existing answer data
                    initial_data = {}
                    question_field_name = f"question_{question.q_id}"

                    if question.q_type in ["open_ended", "datetime", "slider"]:
                        initial_data[question_field_name] = existing_answer.answer_text
                    elif question.q_type == "multiple_choice_single":
                        initial_data[question_field_name] = existing_answer.selected_choice.c_id if existing_answer.selected_choice else None
                    elif question.q_type == "single_choice_other":
                        if existing_answer.selected_choice:
                            initial_data[question_field_name] = existing_answer.selected_choice.c_id
                        elif existing_answer.answer_text:
                            initial_data[question_field_name] = 'other'
                            initial_data[f"{question_field_name}_other"] = existing_answer.answer_text
                    elif question.q_type == "multiple_choice_multiple":
                        initial_data[question_field_name] = [choice.c_id for choice in existing_answer.selected_choices.all()]
                    elif question.q_type == "multiple_choice_other":
                        selected_choices_ids = [choice.c_id for choice in existing_answer.selected_choices.all()]
                        if existing_answer.answer_text:
                            selected_choices_ids.append('other')
                            initial_data[f"{question_field_name}_other"] = existing_answer.answer_text
                        initial_data[question_field_name] = selected_choices_ids
                    elif question.q_type == 'multi_text':
                        # Need to parse the formatted string back into parts
                        if existing_answer.answer_text:
                            parts = existing_answer.answer_text.split(', ')
                            for part in parts:
                                if "Okul: " in part:
                                    initial_data[f"{question_field_name}_part1"] = part.replace("Okul: ", "")
                                elif "Bölüm: " in part:
                                    initial_data[f"{question_field_name}_part2"] = part.replace("Bölüm: ", "")
                                elif "Yıl: " in part:
                                    initial_data[f"{question_field_name}_part3"] = part.replace("Yıl: ", "")
                    elif question.q_type == 'number_range':
                        if existing_answer.answer_text:
                            range_parts = existing_answer.answer_text.split('-')
                            if len(range_parts) == 2:
                                if range_parts[0]:
                                    initial_data[f"{question_field_name}_min"] = int(range_parts[0])
                                if range_parts[1]:
                                    initial_data[f"{question_field_name}_max"] = int(range_parts[1])
                    form = AnswerForm(question=question, request=request, initial=initial_data)
                else:
                    form = AnswerForm(question=question, request=request)
            except UserSession.DoesNotExist:
                form = AnswerForm(question=question, request=request)
        else:
            form = AnswerForm(question=question, request=request)

        # Determine previous question for 'Back' button
        previous_question_obj = Question.objects.filter(
            Q(section__lt=question.section) |
            Q(section=question.section, pk__lt=question.pk)
        ).order_by('-section', '-pk').first()

        if previous_question_obj:
            request.session['previous_question_id'] = previous_question_obj.pk
        else:
            # If it's the first question, ensure previous_question_id is not set
            if 'previous_question_id' in request.session:
                del request.session['previous_question_id']

    all_questions = Question.objects.order_by('section', 'pk')
    answered_question_ids = []
    if request.session.session_key:
        try:
            user_session = UserSession.objects.get(session_key=request.session.session_key)
            answered_question_ids = set(Answer.objects.filter(session=user_session).values_list('question__q_id', flat=True))
        except UserSession.DoesNotExist:
            pass

    return render(request, "answer_form.html", {
        "form": form,
        "question": question,
        "all_questions": all_questions,
        "answered_question_ids": answered_question_ids,
        "expected_field_name": f"question_{question.q_id}",
        "is_16_personalities": (question.text == "16 Personalities"),
        "current_question_number": Question.objects.filter(section=question.section, pk__lt=question.pk).count() + Question.objects.filter(section__lt=question.section).count() + 1,
        "total_questions": all_questions.count()
    })

    all_questions = Question.objects.order_by('section', 'pk')
            
    return render(request, "answer_form.html", {
        "form": form,
        "question": question,
        "all_questions": all_questions,
        "expected_field_name": f"question_{question.q_id}",
        "is_16_personalities": (question.text == "16 Personalities"),
        "current_question_number": Question.objects.filter(pk__lt=question.pk).count() + 1,
        "total_questions": Question.objects.count()
    })

def go_to_question(request, question_id):
    request.session['current_question_id'] = question_id
    return redirect('submit_answer')

def previous_question(request):
    current_question_id = request.session.get('current_question_id')
    if current_question_id is None:
        return redirect('start') # Or some error page

    current_question = get_object_or_404(Question, pk=current_question_id)

    # Find the previous question
    previous_question = Question.objects.filter(
        Q(section__lt=current_question.section) | 
        Q(section=current_question.section, pk__lt=current_question.pk)
    ).order_by('-section', '-pk').first()

    if previous_question:
        request.session['current_question_id'] = previous_question.pk
    else:
        # If no previous question, stay on the first question or redirect to start
        first_question = Question.objects.order_by('section', 'pk').first()
        if first_question:
            request.session['current_question_id'] = first_question.pk
        else:
            return redirect('no_questions')

    return redirect('submit_answer')

def success(request):
    return redirect('results')

def results(request):
    session_key = request.session.session_key
    if not session_key:
        return redirect('start')

    try:
        user_session = UserSession.objects.get(session_key=session_key)
        answers = Answer.objects.filter(session=user_session).order_by('question__section', 'question__pk')
    except UserSession.DoesNotExist:
        return redirect('start')

    return render(request, 'results.html', {
        'user_session': user_session,
        'answers': answers
    })

def no_questions(request):
    return render(request, 'no_questions.html')



def reset_session(request):
    session_key = request.session.session_key
    if session_key:
        try:
            # Delete the UserSession object associated with the current session key
            user_session = UserSession.objects.get(session_key=session_key)
            user_session.delete()
        except UserSession.DoesNotExist:
            pass # No UserSession to delete

    # Clear all session data and generate a new session key
    request.session.flush()
    request.session.create()

    return redirect('start')