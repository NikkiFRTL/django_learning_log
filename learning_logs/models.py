from django.db import models
from django.contrib.auth.models import User


# ОПРЕДЕЛЕНИЕ МОДЕЛЕЙ
# Create your models here.
class Topic(models.Model):
    """ Тема, которую изучает пользователь """
    # Резервируем максимальную длину 200 в базе данных для наполенения названиями тем тем в дальнейшем.
    # CharField - блок данных, состоящий из символов.
    text = models.CharField(max_length=200)

    # DateTimeField - блок данных для хранения даты и времени
    # Аргумент auto_now_add автоматически присваивает атрибуту date_added текущую дату в момент создания темы.
    date_added = models.DateTimeField(auto_now_add=True)

    # Полный список полей Fields со всеми возможностями описаны на сайте ресурсе:
    # https://docs.djangoproject.com/en/2.2/ref/models/fields/

    # Сначала модель User импортируется из django.contrib.auth. Затем в Topic добавляется поле owner,
    # используемое в отношении внешнего ключа к модели User.
    # Чтобы в них отображались только данные, связанные с текущим пользователем
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # Django вызывает метод __str__() для простого представления модели. В описаном случае - строку из атрибута text.
    def __str__(self):
        """ Возвращает строковое представление модели """
        return self.text


class Entry(models.Model):
    """ Информация, изученная пользователем по теме """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """ Возвращает строковое представление модели"""
        if len(self.text) > 50:
            return f"{self.text[:50]}..."
        return self.text
