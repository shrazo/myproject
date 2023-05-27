from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.models import User 

# Create your views here.
from .models import Board, Topic, Post
from .forms import NewTopicForm

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

# # Naive approach
# def new_topic(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     if request.method=='POST':
#         subject = request.POST['subject']
#         message = request.POST['message']

#         user = User.objects.first()
#         topic = Topic.objects.create(
#             subject=subject,
#             board = board,
#             starter=user
#         )
#         post = Post.objects.create(
#             message = message,
#             topic = topic,
#             created_by = user
#         )
#         return redirect('topics', pk=pk)
    
#     context = {
#         'board': board
#     }
#     template = 'boards/new_topic.html'
#     return render(request, template, context)

# Better approach
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()

    if request.method=='POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board 
            topic.starter = user 
            topic.save()
            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                topic = topic,
                created_by = user
            )
            return redirect('topics', pk=board.pk)
    else:
        form = NewTopicForm()
        
    context = {
        'board': board,
        'form': form
    }
    template = 'boards/new_topic.html'
    return render(request, template, context)
