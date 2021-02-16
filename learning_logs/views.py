from django.shortcuts import render
from .models import Topic  # Сначала импортируется модель, связанная с нужными данными


# Create your views here.
def index(request):
    """
    Домашняя страница приложения learning_log
    """
    return render(request, 'learning_logs/index.html')


def topics(request):  # Функции topics() необходим один параметр: объект request, полученный Django от сервера.
    """
    Выводит список тем.
    """
    # Далеев ыдается запрос к базе данных на получение объектов Topic, отсортированных по атрибуту date_added.
    # Полученный итоговый набор сохраняется в topics.
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)  # Контекст.
    # Контекст представляет собой словарь,
    # в котором ключами являются имена, используемые в шаблоне для обращения к данным,
    # а значениями — данные, которые должны передаваться шаблону.

