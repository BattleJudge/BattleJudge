from django.urls import path
from ..views.user_views import (BattleRecordAPI, RankAPI, 
                                BattleSubmissionRecordAPI)

urlpatterns = [
    path('rank/', RankAPI.as_view(), name='rank'),
    path('battle_record/', BattleRecordAPI.as_view(), name='battle_record'),
    path('battle_submissions/', BattleSubmissionRecordAPI.as_view(), name='battle_submission_record')
]