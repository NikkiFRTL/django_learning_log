from django.db import models

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

    # Django вызывает метод __str__() для простого представления модели. В описаном случае - строку из атрибута text.
    def __str__(self):
        """ Возвращает строковое представление модели """
        return self.text
