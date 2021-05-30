import logging
import sys
from datetime import timedelta
sys.path.append('../../')
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny, IsAuthenticated, )
from django.db.models import Q
from utils.api import get_user_and_token_by_jwt_request
from account.models import User, UserProfile
from submission.models import Submission
from ..models import Battle
from ..pagination import (BattleRecordPagination, RankPagination,
                            BattleSubmissionRecordPagination)
from ..serializers import (BattleRecordSerializer, BattleRankSerializer,
                            GetBattleSubmissionRecordSerializer, ReturnBattleSubmissionRecordSerializer)

logger = logging.getLogger(__name__)

class BattleRecordAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user, token = get_user_and_token_by_jwt_request(request)
        user_profile = UserProfile.objects.get(user=user)
        battle_record_list = Battle.objects.filter(Q(player1_id=user.id) | Q(player2_id=user.id)).order_by('-create_time')
        page_data = BattleRecordPagination().paginate_queryset(battle_record_list, request, self)
        data = BattleRecordSerializer(page_data, many=True).data
        for record in data:
            if record['player1_id'] == user.id:
                record['player1_nickname'] = user_profile.nickname
                try:
                    player2 = User.objects.get(id=record['player2_id'])
                    player2_profile = UserProfile.objects.get(user=player2)
                    record['player2_nickname'] = player2_profile.nickname
                    if record['result'] == 'player1':
                        record['result'] = record['player1_nickname']
                    elif record['result'] == 'player2':
                        record['result'] = record['player2_nickname']
                except Exception as e:
                    record['player2_nickname'] = 'unknow'
                    if record['result'] == 'player1':
                        record['result'] = record['player1_nickname']
                    elif record['result'] == 'player2':
                        record['result'] = record['player2_nickname']
            else:
                record['player1_nickname'] = user_profile.nickname
                try:
                    player2 = User.objects.get(id=record['player1_id'])
                    player2_profile = UserProfile.objects.get(user=player2)
                    record['player2_nickname'] = player2_profile.nickname
                    if record['result'] == 'player1':
                        record['result'] = record['player2_nickname']
                    elif record['result'] == 'player2':
                        record['result'] = record['player1_nickname']
                except Exception as e:
                    record['player2_nickname'] = 'unknow'
                    if record['result'] == 'player1':
                        record['result'] = record['player2_nickname']
                    elif record['result'] == 'player2':
                        record['result'] = record['player1_nickname']
            record.pop('player1_id')
            record.pop('player2_id')

        resp_data = {}
        resp_data['total'] = battle_record_list.count()
        resp_data['data'] = data
        return Response(data=resp_data)


class RankAPI(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        size = request.GET.get('size', default=20)
        page = request.GET.get('page', default=1)
        user_list = UserProfile.objects.all().order_by('-battle_score')
        page_data = RankPagination().paginate_queryset(user_list, request, self)
        data = BattleRankSerializer(page_data, many=True).data

        page = int(page)
        size = int(size)
        rank = (page - 1) * size
        for v in data:
            rank += 1
            v['rank'] = rank
            if v['battle_win'] + v['battle_lose'] == 0:
                v['rate'] = round(0.00, 2)
            else:
                v['rate'] = round(v['battle_win'] / (v['battle_win'] + v['battle_lose']), 2)
        
        resp_data = {}
        resp_data['total'] = user_list.count()
        resp_data['data'] = data
        return Response(data=resp_data)


class BattleSubmissionRecordAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        resp_data = {'code': 0, 'msg': 'success', 'data': {}}

        serializer = GetBattleSubmissionRecordSerializer(data=request.GET)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(data=resp_data)
        logger.debug("222")
        user, token = get_user_and_token_by_jwt_request(request)
        submissions = Submission.objects.filter(battle_id=serializer.data['battle_id'], user_id=user.id).order_by('-create_time')
        page_data = BattleSubmissionRecordPagination().paginate_queryset(submissions, request, self)
        data = ReturnBattleSubmissionRecordSerializer(page_data, many=True).data

        resp_data = {}
        resp_data['total'] = submissions.count()
        resp_data['data'] = data
        return Response(data=resp_data)