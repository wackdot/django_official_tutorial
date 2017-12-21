from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    # ex: /polls/
    path('', views.IndexView.as_view(), name='index'),
    # The generic DetailView expects the primary key captured from the URL to be called 'pk'
    # ex: /polls/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'), 
    # ex: /polls/5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]