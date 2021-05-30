from django.urls import path
from ..views.user_views import (SubmissionAPI, SubmissionListAPI)

urlpatterns = [
    path('submission/', SubmissionAPI.as_view(), name='user_submission'),
    path('submission_list/', SubmissionListAPI.as_view(), name='user_submission_list'),
]