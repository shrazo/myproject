from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.db.models import Count 

# Create your views here.
from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm

def home(request):
    boards = Board.objects.all()
    context = {
        'boards': boards
    }
    template = 'boards/home.html'
    return render(request, template, context)

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts')-1)
    context = {
        'board':board,
        'topics': topics, 
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
@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()

    if request.method=='POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board 
            topic.starter = request.user 
            topic.save()
            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                topic = topic,
                created_by = request.user 
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

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    context = {
        'topic': topic,
    }
    template = 'boards/topic_posts.html'
    return render(request, template, context)

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    
    if request.method=='POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic 
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    context = {
        'topic': topic,
        'form': form
    }
    template = 'boards/reply_topic.html'
    return render(request, template, context)