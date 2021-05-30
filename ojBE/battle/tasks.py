from __future__ import absolute_import, unicode_literals
import logging
from oj.celery import app
from random import shuffle, sample
from django.utils.timezone import now
from problem.models import Problem
from account.models import User, UserProfile
from .consumers import send_battle_connect_info
from .models import Battle, BattleUser

logger = logging.getLogger(__name__)

@app.task
def battle_connect():
    try:
        b_users = BattleUser.objects.filter(waiting=True)
        cnt = b_users.count()
        b_users_id = []
        for user in b_users:
            b_users_id.append(user.user_id)
        shuffle(b_users_id)

        problems = Problem.objects.filter(in_battle_set=True)
        problems_id = []
        for pro in problems:
            problems_id.append(pro.id)
        
        if len(problems_id) == 0:
            return

        n = None
        if cnt % 2 == 0:
            n = int(cnt / 2)
        else:
            n = int((cnt - 1) / 2)
        for i in range(n):
            first_id = b_users_id[i]
            second_id = b_users_id[2 * i + 1]
            player1 = BattleUser.objects.get(user_id=first_id)
            player2 = BattleUser.objects.get(user_id=second_id)
            player1.opponent_channels_name = player2.channels_name
            player2.opponent_channels_name = player1.channels_name
            player1.waiting = False
            player2.waiting = False

            pro_id = sample(problems_id, 1)[0]

            battle = Battle.objects.create(
                player1_id=player1.user_id,
                player2_id=player2.user_id,
                player1_code='',
                player2_code='',
                player1_endtime=now(),
                player2_endtime=now(),
                pro_id=pro_id,
                result=''
            )

            player1.battle_id = battle.id
            player2.battle_id = battle.id

            player1.save()
            player2.save()

            send_battle_connect_info(player1.channels_name, player2.user_id)
            send_battle_connect_info(player2.channels_name, player1.user_id)
    except Exception as e:
        logger.exception(e)