from django.urls import path
from ..views.user_views import (ProblemAPI, ProblemListAPI, 
                                SolutionListAPI, SolutionAPI, )

urlpatterns = [
    path('problem_list/', ProblemListAPI.as_view(), name='user_problem_list'),
    path('problem/', ProblemAPI.as_view(), name='user_problem'),
    path('solution_list/', SolutionListAPI.as_view(), name='solution_list'),
    path('solution/', SolutionAPI.as_view(), name='solution'),
]