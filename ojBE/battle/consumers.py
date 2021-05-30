import logging
import json
from urllib import parse
from django.utils.timezone import now
from channels.generic.websocket import JsonWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from utils.api import get_user_by_ws
from account.models import UserProfile
from judge.tasks import battle_judge
from submission.models import JudgeStatus
from account.models import UserProfile, User
from problem.models import Problem
from problem.serializers import UserGetProblemInfoSerializer
from .models import BattleUser, Battle, BattleResult

logger = logging.getLogger(__name__)

def send_battle_connect_info(player_channels_name, opponent_user_id):
    data = {'msg': 'success', 'opponent_user_id': opponent_user_id}
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.send)(player_channels_name, {
        'type': 'send.battle.info',
        'text': json.dumps(data)
    })


class BattleConsumer(WebsocketConsumer):
    def connect(self):
        try:
            url = "ws://127.0.0.1:80" + self.scope['path']
            query_string = bytes.decode(self.scope['query_string'])
            if query_string:
                url = url + "?" + query_string
            url_res = parse.urlparse(url)
            query_dict = parse.parse_qs(url_res.query)
            jwt = query_dict.get("authorization", '')
            if isinstance(jwt, list):
                jwt = jwt[0]
            jwt = "JWT " + jwt
            self.scope['headers'].append((b'authorization', jwt.encode('utf-8')))
            try:
                self.user = get_user_by_ws(self.scope['headers'])
            except Exception as e:
                logger.exception(e)
                self.close(3001)
                return
            if BattleUser.objects.filter(user_id=self.user.id).exists():
                self.close(3002)
                return
            self.battle_user = BattleUser.objects.create(
                user_id=self.user.id,
                channels_name=self.channel_name,
                pro_id=0,
                opponent_channels_name="",
                battle_id=0
            )
            self.accept()
            self.send(json.dumps("connect accept"))
        except Exception as e:
            logger.exception(e)

    def disconnect(self, code):
        # if user in the battle
        try:
            if not self.battle_user.waiting:
                battle = Battle.objects.get(id=self.battle_user.battle_id)
                # the battle not over
                if not battle.result:
                    user_profile = UserProfile.objects.get(user=self.user)
                    user_profile.battle_score = max(0, user_profile.battle_score - 10)
                    user_profile.battle_lose += 1
                    user_profile.save()
                    battle.result = BattleResult.DRAWN_GAME
                    if battle.player1_id == self.battle_user.user_id:
                        battle.player1_endtime = now()
                    else:
                        battle.player2_endtime = now()
                    battle.save()

                    content = {'msg': 'draw'}
                    self.channel_layer = get_channel_layer()
                    async_to_sync(self.channel_layer.send)(self.battle_user.opponent_channels_name, {
                        "type": "battle.result.handler",
                        "text": json.dumps(content),
                    })
            BattleUser.objects.filter(user_id=self.user.id).delete()
        except Exception as e:
            logger.exception(e)

    def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
            if not isinstance(data, dict):
                resp_data = {'code': -1, 'msg': 'request data error', 'data': {}}
                self.send(json.dumps(resp_data))
                return
            if not 'op' in data:
                resp_data = {'code': -1, 'msg': 'request data error', 'data': {}}
                self.send(json.dumps(resp_data))
                return
            op = data['op']
            if op == 'submit':
                if not 'code' in data or not 'language' in data:
                    resp_data = {'code': -1, 'msg': 'request data error', 'data': {}}
                    self.send(json.dumps(resp_data))
                    return
                code = data['code']
                language = data['language']
                text_data = {'code': code, 'language': language}
                async_to_sync(self.channel_layer.send)(self.channel_name, {
                    "type": "battle.judge",
                    "text": json.dumps(text_data),
                })
                return
            else:
                resp_data = {'code': -1, 'msg': 'request data error', 'data': {}}
                self.send(json.dumps(resp_data))
                return
        except Exception as e:
            logger.exception(e)

    def battle_judge(self, data):
        try:
            data = json.loads(data['text'])
            if self.battle_user.waiting:
                resp_data = {'code': -2, 'msg': 'you are not in the battle', 'data': {}}
                self.send(json.dumps(resp_data))
                return
            
            battle = Battle.objects.get(id=self.battle_user.battle_id)
            if battle.result:
                resp_data = {'code': -3, 'msg': 'the battle is over', 'data': {}}
                self.send(json.dumps(resp_data))
                return
            if battle.player1_id == self.battle_user.user_id:
                battle.player1_code = data['code']
                battle.player1_endtime = now()
            else:
                battle.player2_endtime = now()
                battle.player2_code = data['code']
            battle.save()
            data['user_id'] = self.battle_user.user_id
            data['problem_id'] = battle.pro_id
            data['battle_id'] = self.battle_user.battle_id
            resp = battle_judge(data)

            # AC handling
            if not battle.result and 'result' in resp['data'] and resp['data']['result'] == JudgeStatus.ACCEPTED:
                user_profile = UserProfile.objects.get(user=self.user)
                user_profile.battle_score = min(9999, user_profile.battle_score + 10)
                user_profile.battle_win += 1
                user_profile.save()

                if battle.player1_id == self.battle_user.user_id:
                    battle.result = BattleResult.PLAYER1_WIN
                else:
                    battle.result = BattleResult.PLAYER2_WIN
                battle.save()

                content = {'msg': 'lose', 'code': data['code']}
                self.channel_layer = get_channel_layer()
                async_to_sync(self.channel_layer.send)(self.battle_user.opponent_channels_name, {
                    "type": "battle.result.handler",
                    "text": json.dumps(content),
                })

            self.send(json.dumps(resp))
        except Exception as e:
            logger.exception(e)

    def battle_result_handler(self, data):
        try:
            data = json.loads(data['text'])
            msg = data['msg']
            resp_data = {'code': 0, 'msg': msg, 'data': {}}
            if msg == 'lose':
                user_profile = UserProfile.objects.get(user=self.user)
                user_profile.battle_score = max(0, user_profile.battle_score - 5)
                user_profile.battle_lose += 1
                user_profile.save()
                resp_data['data']['winner_code'] = data['code']
                self.send(json.dumps(resp_data))
            elif msg == 'draw':
                self.send(json.dumps(resp_data))
        except Exception as e:
            logger.exception(e)

    def send_battle_info(self, text):
        try:
            text = json.loads(text['text'])
            if text['msg'] == 'success':
                resp_data = {'code': 0, 'msg': 'connect success', 'data': {}}
                b_user = BattleUser.objects.get(user_id=self.battle_user.user_id)
                self.battle_user = b_user
                battle = Battle.objects.get(id=b_user.battle_id)
                problem = Problem.objects.get(id=battle.pro_id)
                pro_data = UserGetProblemInfoSerializer(problem).data
                resp_data['data']['problem_data'] = pro_data

                opponent_user = User.objects.get(id=text['opponent_user_id'])
                opponent_user_profile = UserProfile.objects.get(user=opponent_user)
                resp_data['data']['opponent_info'] = {}
                resp_data['data']['opponent_info']['nickname'] = opponent_user_profile.nickname

                self.send(json.dumps(resp_data))
        except Exception as e:
            logger.exception(e)
            