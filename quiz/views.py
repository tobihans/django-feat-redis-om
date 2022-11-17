from django.core.exceptions import BadRequest
from django.http import HttpResponse
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
    return HttpResponse(pk)
