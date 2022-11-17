import redis_om
from django.core.exceptions import BadRequest
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from quiz.forms import QuizCreationForm
from quiz.redis_models import SimpleQuiz


def index(request):
    pks = list(SimpleQuiz.all_pks())
    quizzes = [SimpleQuiz.get(pk) for pk in pks]
    return render(request, "quiz/index.html", {"quizzes": quizzes})


@require_http_methods(["GET", "POST"])
def create(request):
    if request.method == "GET":
        return render(request, "quiz/create.html")

    if (form := QuizCreationForm(request.POST)).is_valid():
        quiz = SimpleQuiz(**form.cleaned_data)
        quiz.save()

        return redirect(reverse("quiz_detail", args=(quiz.pk,)))
    raise BadRequest()


def detail(request, pk: str):
    try:
        quiz = SimpleQuiz.get(pk)

        if request.method == "GET":
            return render(request, "quiz/quiz.html", {"quiz": quiz})

        is_success = quiz.correct_option.value == request.POST.get("correct_option")
        request.session[f"{quiz.pk}_has_succeeded"] = is_success
        quiz.nb_of_successful_attempts += int(is_success)
        quiz.nb_of_failed_attempts += int(not is_success)
        quiz.save()

        return redirect(reverse("quiz_result", args=[quiz.pk]))

    except redis_om.NotFoundError as e:
        raise Http404() from e


def result(request, pk):
    has_succeeded = request.session.get(f"{pk}_has_succeeded")

    if has_succeeded is not None:
        return render(request, "quiz/result.html", {"has_succeeded": has_succeeded})

    raise Http404()
