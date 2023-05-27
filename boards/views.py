from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.models import User 

# Create your views here.
from .models import Board, Topic, Post

def home(request):
    boards = Board.objects.all()
    context = {
        'boards': boards
    }
    template = 'boards/home.html'
    return render(request, template, context)

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    
    context = {
        'board':board
    }
    template = 'boards/topics.html'
    return render(request, template, context)

def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method=='POST':
        subject = request.POST['subject']
        message = request.POST['message']

        user = User.objects.first()
        topic = Topic.objects.create(
            subject=subject,
            board = board,
            starter=user
        )
        post = Post.objects.create(
            message = message,
            topic = topic,
            created_by = user
        )
        return redirect('topics', pk=pk)
    
    context = {
        'board': board
    }
    template = 'boards/new_topic.html'
    return render(request, template, context)
