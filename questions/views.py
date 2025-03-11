from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Question, Answer, Choice, UserSession
from .forms import AnswerForm
from django.db.transaction import atomic

def start_questionnaire(request):
    # Start with the first question
    first_question = Question.objects.order_by('section', 'pk').first()
    if first_question is None:
        return redirect('no_questions')
    return redirect('submit_answer')

def submit_answer(request, question_id=None):
    if question_id is None:
        question = Question.objects.order_by("section","pk").first()
        if question is None:
            return render(request, "no_questions.html")
    else:
        question = get_object_or_404(Question, pk=question_id)
    
    if request.method == "POST":
        form = AnswerForm(request.POST, question=question, request=request)
        print("Form data:", request.POST)  # Debug print
        print("Form is valid:", form.is_valid())  # Debug print
        if not form.is_valid():
            print("Form errors:", form.errors)  # Debug print
        
        if form.is_valid():
            try:
                with atomic():
                    answer = form.save(commit=False, request=request)
                    answer.question = question
                    answer.save()

                next_question = Question.objects.filter(section=question.section,
                                                        pk__gt=question.pk).order_by("pk").first()
                
                if next_question:
                    return redirect("submit_answer", question_id=next_question.pk)
                else:
                    next_section_question = Question.objects.filter(
                        section__gt=question.section
                    ).order_by("section","pk").first()
                    
                    if next_section_question:
                        return redirect("submit_answer", question_id=next_section_question.pk)
                    else:
                        return redirect("success")
            except Exception as e:
                print("Error saving form:", str(e))  # Debug print
                raise
    else:
        form = AnswerForm(question=question, request=request)
    
    return render(request, "answer_form.html", {
        "form": form,
        "question": question,
        "current_question_number": Question.objects.filter(pk__lt=question.pk).count() + 1,
        "total_questions": Question.objects.count()
    })

def success(request):
    return render(request, 'success.html')

def no_questions(request):
    return render(request, 'no_questions.html')

def view_all_responses(request, admin_password=None):
    # Simple password protection - you can set this as an environment variable
    if admin_password != '123':  # Replace with a secure password
        return HttpResponse("Unauthorized", status=401)
    
    # Get all unique respondents
    respondents = UserSession.objects.all()
    
    all_responses = []
    for session in respondents:
        user_answers = Answer.objects.filter(session=session).order_by('question__section', 'question__pk')
        
        response_data = {
            'user_name': session.nickname,
            'contact_info': session.contact_info,
            'answers': []
        }
        
        for answer in user_answers:
            answer_data = {
                'question': answer.question.text,
                'section': answer.question.section,
                'type': answer.question.q_type,
                'response': None
            }
            
            # Format answer based on question type
            if answer.question.q_type == 'open_ended':
                answer_data['response'] = answer.answer_text
            elif answer.question.q_type == 'multiple_choice_single':
                answer_data['response'] = answer.selected_choice.text if answer.selected_choice else None
            elif answer.question.q_type == 'multiple_choice_multiple':
                answer_data['response'] = [choice.text for choice in answer.selected_choices.all()]
            
            response_data['answers'].append(answer_data)
        
        all_responses.append(response_data)
    
    return render(request, 'admin_view_responses.html', {
        'responses': all_responses
    })