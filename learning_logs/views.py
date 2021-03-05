from django.shortcuts import render, redirect, get_object_or_404  # HttpResponseRedirect который будет использоваться
# для перенаправления
# пользователя к странице topics после отправки введенной темы.
from django.contrib.auth.decorators import login_required
# Импортируем исключение Http404, которое будет выдаваться программой при запросе пользователем темы,
# которую ему видеть не положено.
from django.http import Http404
from .models import Topic, Entry  # Импортируется модели, связанные с нужными данными
from .forms import TopicForm, EntryForm


# Создание Предствлений (views)
def index(request):
    """
    Домашняя страница приложения learning_log
    """
    return render(request, 'learning_logs/index.html')


# Декоратор login_required() проверяет, вошел ли пользователь в систему, и Django запускает код topics() только
# при выполнении этого условия. Если же пользователь не выполнил вход, он перенаправляется на страницу входа.
@login_required
def topics(request):  # Функции topics() необходим один параметр: объект request, полученный Django от сервера.
    """
    Выводит список тем.
    """
    # Далее выдается запрос к базе данных на получение объектов Topic, отсортированных по атрибуту date_added.
    # Полученный итоговый набор сохраняется в topics.
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')

    # Контекст представляет собой словарь,
    # в котором ключами являются имена, используемые в шаблоне для обращения к данным,
    # а значениями — данные, которые должны передаваться шаблону.
    context = {'topics': topics}

    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    # Функция получает значение, совпавшее с выражением /<int:topic_id>/ и сохраняет его в topic_id.
    """
    Выводит одну тему и все ее записи.
    """
    # Функция get() используется для получения темы.
    topic = get_object_or_404(Topic, id=topic_id)

    # Проверка того, что тема принадлежит текущему пользователю.
    check_topic_owner(topic, request)

    # Загружаются записи, связанные с данной темой, и они
    # упорядочиваются по значению date_added: знак «минус» перед date_added сортирует результаты вобратном порядке.
    entries = topic.entry_set.order_by('-date_added')

    # Тема и записи сохраняются в словаре context, который передается шаблону topic.html.
    context = {'topic': topic, 'entries': entries}

    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Определяет новую тему."""
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = TopicForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = TopicForm(data=request.POST)
        # Проверка на правильность заполнения.
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    # Вывести пустую или недействительную форму.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Добавляет новую запись по конкретной теме."""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = EntryForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = EntryForm(data=request.POST)
        # Проверка на правильность заполнения.
        if form.is_valid():

            # При вызове save() мы включаем аргумент commit=False для того, чтобы создать новый объект записи
            # и сохранить его в new_entry, не сохраняя пока в базе данных.
            new_entry = form.save(commit=False)

            new_entry.topic = topic

            # Проверка того, что тема принадлежит текущему пользователю.
            check_topic_owner(topic, request)

            # Запись сохраняется в базе данных с правильно ассоциированной темой topic.
            new_entry.save()

            # Получает два аргумента — имя представления, которому передается управление,
            # и аргумент для функции представления.
            # Вызов перенаправляет пользователя на страницу темы, для которой была создана запись.
            return redirect('learning_logs:topic', topic_id=topic_id)

    # Вывести пустую или недействительную форму.
    context = {'topic': topic, 'form': form}

    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Редактирует существующую запись."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    # Проверка того, что тема принадлежит текущему пользователю.
    check_topic_owner(topic, request)

    if request.method != 'POST':
        # Этот аргумент приказывает Django создать форму, заранее заполненную информацией из существующего
        # объекта записи. Пользователь видит свои существующие данные и может отредактировать их.
        form = EntryForm(instance=entry)
    else:
        # Аргументы риказывают Django создать экземпляр формы на основании информации существующего объекта записи,
        # обновленный данными из request.POST
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    # Если отображается исходная форма для редактирования записи или если отправленная форма недействительна,
    # создается словарь context, а страница строится на базе шаблона edit_entry.html.
    context = {'entry': entry, 'topic': topic, 'form': form}

    return render(request, 'learning_logs/edit_entry.html', context)


def check_topic_owner(topic, request):
    # Проверка того, что тема принадлежит текущему пользователю.
    if topic.owner != request.user:
        raise Http404
