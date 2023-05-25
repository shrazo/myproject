from django.shortcuts import render, HttpResponse

# Create your views here.
from .models import Board

def home(request):
    boards = Board.objects.all()
    context = {
        'boards': boards
    }
    template = 'boards/home.html'

    return render(request, template, context)