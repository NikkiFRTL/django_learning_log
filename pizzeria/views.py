from django.shortcuts import render


# Create your views here.
def pizza_index(request):
    """
    Домашняя страница приложения pizzeria
    """
    return render(request, 'pizzeria/pizza_index.html')
