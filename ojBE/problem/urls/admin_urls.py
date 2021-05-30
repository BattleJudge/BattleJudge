from django.urls import path
from ..views.admin_views import (ProblemListAPI, ProblemAPI,
                                ProblemTagAPI, ProblemTestCaseAPI, )

urlpatterns = [
    path('problem_list/', ProblemListAPI.as_view(), name='admin_problem_list'),
    path('problem/', ProblemAPI.as_view(), name='admin_problem'),
    path('problem_tag/', ProblemTagAPI.as_view(), name='admin_problem_tag'),
    path('testcase/', ProblemTestCaseAPI.as_view(), name='admin_upload_test_case'),
]