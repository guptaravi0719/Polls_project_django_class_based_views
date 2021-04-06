from django.shortcuts import render, redirect
from django.http import HttpResponse, response
from rest_framework.views import APIView
from .forms import CreatePollForm
from .models import Poll
from rest_framework import mixins
from rest_framework import generics
from rest_framework.generics import ListAPIView, ListCreateAPIView
from .serializers import PollSerializer, VoteViewOptionSerializer, ResultSerializer
from .models import Poll

# CLASS BASED VIEW

class HomeView(ListCreateAPIView):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()

class Create(APIView):
    def get(self,request):
        form = CreatePollForm()
        context = {
            'form': form
        }

        return render(request, "poll/create.html", context)

    def post(self, request):
        form = CreatePollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')



class Vote(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,generics.GenericAPIView,mixins.ListModelMixin):

    queryset = Poll.objects.all()
    serializer_class = VoteViewOptionSerializer
    lookup_field = 'poll_id'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)



def voted(request, poll_id, option_no):
    poll = Poll.objects.get(pk=poll_id)

    if option_no == 1:
        poll.option_one_count += 1
    elif option_no == 2:
        poll.option_two_count += 1
    elif option_no == 3:
        poll.option_three_count += 1
    else:
        return HttpResponse(400, 'Invalid Request')
    poll.save()
    return redirect('results', poll_id)


class Result(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,generics.GenericAPIView,mixins.ListModelMixin):
    queryset = Poll.objects.all()
    serializer_class = ResultSerializer
    lookup_field = 'poll_id'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


# ##############################################################################################################################################
# BELOW IS THE FUNCTION BASED VIEW REPRESENTATION OF THE PROJECT VIEWS


# def home(request):
#     polls = Poll.objects.all()
#     html = "<html><body><div>Sorry No polls Available Now . Better You create one by clicking here :  <a href='create'> Create a Poll</a></div> </br></body></html>"
#     if len(polls) == 0:
#         return HttpResponse(html)
#     else:
#         context = {'polls': polls}
#         return render(request, 'poll/home.html', context)

#         # passing data to template, polls in template will get value as Polls.objects.all()

#
# def create(request):
#     if request.method == 'POST':
#         form = CreatePollForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#
#     else:
#         form = CreatePollForm()
#
#     context = {
#         'form': form
#     }
#
#     return render(request, "poll/create.html", context)



#
# def vote(request, poll_id):
#     poll = Poll.objects.get(pk=poll_id)
#     if request.method == 'POST':
#         selected_option = request.POST['poll']
#         if selected_option == 'option1':
#             poll.option_one_count += 1
#
#         elif selected_option == 'option2':
#             poll.option_two_count += 1
#
#         elif selected_option == 'option3':
#             poll.option_three_count += 1
#         else:
#             return HttpResponse(400, 'invalid form')
#
#         poll.save()
#         return redirect('results', poll.id)
#
#     context = {'poll': poll}  # saving data for use in template
#
#     return render(request, 'poll/vote.html', context)
#
#


# def results(request, poll_id):
#     # dictionary for initial data with
#     # field names as keys
#     context = {}
#
#     # add the dictionary during initialization
#     context["poll"] = Poll.objects.get(pk=poll_id)
#
#     return render(request, "poll/results.html", context)