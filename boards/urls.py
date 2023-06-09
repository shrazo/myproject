from django.urls import path
from . import views 
urlpatterns = [
    path("", views.home, name="home"),
    path("<int:pk>/", views.board_topics, name="topics"),
    path("<int:pk>/new/", views.new_topic, name="new_topic"),
    path("<int:pk>/topics/<topic_pk>/", views.topic_posts, name="topic_posts"),
    path("<int:pk>/topics/<topic_pk>/reply", views.reply_topic, name="reply_topic"),
]
