
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Option, Attempt
from .forms import QuizForm, QuestionAndOptionsForm
from django.views.decorators.http import require_POST

def root_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('quiz_list')
    else:
        return redirect('login')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('quiz_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('quiz_list')
    quizzes = Quiz.objects.filter(creator=request.user)
    total_questions = Question.objects.filter(quiz__in=quizzes).count()
    total_attempts = Attempt.objects.filter(quiz__in=quizzes).count()

    context = {
        'quizzes': quizzes,
        'total_questions': total_questions,
        'total_attempts': total_attempts
    }
    return render(request, 'quiz/admin_dashboard.html', context)

@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

@login_required
def quiz_detail(request, pk):
    quiz = get_object_or_404(Quiz.objects.prefetch_related('questions__options'), pk=pk)
    questions = quiz.questions.all()
    return render(request, 'quiz/quiz_detail.html', {'quiz': quiz, 'questions': questions})

@login_required
def quiz_submit(request, pk):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz.objects.prefetch_related('questions__options'), pk=pk)
        score = 0
        total_questions = quiz.questions.count()

        for question in quiz.questions.all():
            selected_option_id = request.POST.get(f'question_{question.id}')
            if selected_option_id:
                if question.correct_option and question.correct_option.id == int(selected_option_id):
                    score += 1

        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        attempt = Attempt.objects.create(user=request.user, quiz=quiz, score=score)

        return render(request, 'quiz/quiz_result.html', {
            'quiz': quiz,
            'score': score,
            'total_questions': total_questions,
            'percentage': percentage,
            'attempt': attempt
        })
    return redirect('quiz_detail', pk=pk)

@login_required
def quiz_add(request):
    if not request.user.is_staff:
        return redirect('quiz_list')
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.creator = request.user
            quiz.save()
            return redirect('question_add', quiz_pk=quiz.pk)
    else:
        form = QuizForm()
    return render(request, 'quiz/quiz_form.html', {'form': form})

@login_required
def quiz_edit(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if not request.user.is_staff or request.user != quiz.creator:
        return redirect('quiz_list')
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('quiz_list')
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'quiz/quiz_form.html', {'form': form})

@login_required
def quiz_delete(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if not request.user.is_staff or request.user != quiz.creator:
        return redirect('quiz_list')
    if request.method == 'POST':
        quiz.delete()
        return redirect('quiz_list')
    return render(request, 'quiz/quiz_confirm_delete.html', {'quiz': quiz})

@login_required
def question_add(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    if not request.user.is_staff or request.user != quiz.creator:
        return redirect('quiz_detail', pk=quiz_pk)
    if request.method == 'POST':
        form = QuestionAndOptionsForm(request.POST)
        if form.is_valid():
            question = Question.objects.create(quiz=quiz, text=form.cleaned_data['question_text'])
            options = []
            for i in range(1, 5):
                option_text = form.cleaned_data[f'option{i}']
                option = Option.objects.create(question=question, text=option_text)
                options.append(option)
            correct_option_index = int(form.cleaned_data['correct_answer']) - 1
            question.correct_option = options[correct_option_index]
            question.save()
            return redirect('question_add', quiz_pk=quiz.pk)
    else:
        form = QuestionAndOptionsForm()
    return render(request, 'quiz/question_form.html', {'form': form, 'quiz': quiz})

@login_required
def question_edit(request, quiz_pk, pk):
    question = get_object_or_404(Question, pk=pk, quiz__pk=quiz_pk)
    if not request.user.is_staff or request.user != question.quiz.creator:
        return redirect('quiz_detail', pk=quiz_pk)
    if request.method == 'POST':
        form = QuestionAndOptionsForm(request.POST)
        if form.is_valid():
            question.text = form.cleaned_data['question_text']
            question.save()
            # Because there is no is_correct field in the option model I will delete the old options and create new ones
            question.options.all().delete()
            options = []
            for i in range(1, 5):
                option_text = form.cleaned_data[f'option{i}']
                option = Option.objects.create(question=question, text=option_text)
                options.append(option)
            correct_option_index = int(form.cleaned_data['correct_answer']) - 1
            question.correct_option = options[correct_option_index]
            question.save()
            return redirect('quiz_detail', pk=quiz_pk)
    else:
        initial_data = {
            'question_text': question.text,
        }
        correct_option_index = 0
        for i, option in enumerate(question.options.all()):
            initial_data[f'option{i+1}'] = option.text
            if option == question.correct_option:
                correct_option_index = i + 1
        initial_data['correct_answer'] = str(correct_option_index)
        form = QuestionAndOptionsForm(initial=initial_data)

    return render(request, 'quiz/question_form.html', {'form': form, 'quiz': question.quiz})


@login_required
def question_delete(request, quiz_pk, pk):
    question = get_object_or_404(Question, pk=pk)
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    if not request.user.is_staff or request.user != quiz.creator:
        return redirect('quiz_detail', pk=quiz_pk)
    if request.method == 'POST':
        question.delete()
        return redirect('quiz_detail', pk=quiz_pk)
    return render(request, 'quiz/question_confirm_delete.html', {'question': question, 'quiz': quiz})