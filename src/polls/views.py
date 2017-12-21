from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.urls import reverse
from django.views import generic 

from .models import Choice, Question

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)

# def detail(request, question_id):
#     question =  get_object_or_404(Question, pk=question_id)
#     context = {'question': question}
#     return render(request, 'polls/detail.html', context)

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     context = {'question': question}
#     return render(request, 'polls/results.html', context)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        #request.POST['choice'] will raise KeyError if choice wasn’t provided in POST data. 
        # The above code checks for KeyError and redisplays the question form with an error 
        # message if choice isn’t given.
        selected_choice = question.choice_set.get(pk=request.POST['choice']) 
    except (KeyError, Choice.DoesNotExist):
        # Redisply the question voting form.
        context = {
            'question': question, 
            'error_message': "You didn't select a choice", 
        }
        return render(request, 'polls/detail.html', context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

class IndexView(generic.ListView):

    # Default: Uses the template <app name>/<model name>_list.html
    # Overrides default template location
    template_name = 'polls/index.html'

    # Override the default context variable name (question_list)
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            # returns a queryset containing Questions whose pub_date is less than or equal to - that is, 
            # earlier than or equal to - timezone.now.
            pub_date__lte = timezone.now() 
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView): 

    model = Question # Each generic view needs to know which model it will act upon

    # Default context variable name (question)

    # Default: Uses the template <app name>/<model name>_detail.html 
    # Overrides default template location
    template_name = 'polls/detail.html' 

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):

    model = Question                     # Assigns model to view
    template_name = 'polls/results.html' # Override default template url



