import requests
import hashlib
import json
import logging
import django_redis
import sys
sys.path.append("../../")
from django.db import transaction
from account.models import User, UserProfile
from problem.models import Problem
from submission.models import Submission, JudgeStatus
from conf.project_conf import JUDGE_TOKEN, JUDGE_URL
from .languages import languages


logger = logging.getLogger(__name__)

def process_submission_in_redis():
    Cache = django_redis.get_redis_connection()
    if Cache.llen("waiting_queue"):
        from judge.tasks import judge
        submit_data = Cache.rpop("waiting_queue")
        if submit_data:
            submit_data = json.loads(submit_data.decode("utf-8"))
            judge(**submit_data)


class BaseHandler(object):
    def __init__(self):
        self.ori_token = JUDGE_TOKEN
        self.hash_handler = hashlib.sha256()
        self.hash_handler.update(self.ori_token.encode())
        self.token = self.hash_handler.hexdigest()
        self.headers = {"Content-Type": "application/json", "X-Judge-Server-Token": self.token}
        self.url = JUDGE_URL

    def _request(self, data):
        try:
            res = requests.post(self.url, data=json.dumps(data), headers=self.headers).json()
            return res
        except Exception as e:
            logger.exception(e)
            return {'code': -999, 'msg': 'exception'}



class JudgeHandler(BaseHandler):
    def __init__(self, submission_id, problem_id):
        super().__init__()
        self.submission = Submission.objects.get(id=submission_id)
        self.problem = Problem.objects.get(id=problem_id)

    def _static_info_handler(self, data):
        info = {}
        info['time_cost'] = max([x['cpu_time'] for x in data])
        info['memory_cost'] = max([x['memory'] for x in data])
        self.submission.static_info = info

    def judge(self):
        language = self.submission.language
        config = list(filter(lambda item: language == item["name"], languages))[0]
        code = self.submission.code
        data = {
            "src": code,
            "language_config": config['config'],
            "max_cpu_time": self.problem.time_limit,
            "max_memory": 1024 * 1024 * self.problem.memory_limit,
            "test_case_id": str(self.problem.id),
            "output": False,
        }

        Submission.objects.filter(id=self.submission.id).update(result=JudgeStatus.JUDGING)
        resp = self._request(data)
        if not resp:
            Submission.objects.filter(id=self.submission.id).update(result=JudgeStatus.SYSTEM_ERROR)
            return

        if 'code' in resp.keys():
            # put this submission into the redis
            submit_data = {"submission_id": self.submission.id, "problem_id": self.problem.id}
            Cache = django_redis.get_redis_connection()
            Cache.lpush("waiting_queue", json.dumps(submit_data))
            return
        elif resp['err']:
            self.submission.result = JudgeStatus.COMPILE_ERROR
            info = {'err_info': resp['data']}
            self.submission.static_info = info
        else:
            resp["data"].sort(key=lambda x: int(x["test_case"]))
            self.submission.info = resp
            self._static_info_handler(resp['data'])
            error_test_case = list(filter(lambda case: case["result"] != 0, resp["data"]))
            if not error_test_case:
                self.submission.result = JudgeStatus.ACCEPTED
            else:
                self.submission.result = error_test_case[0]["result"]

        self.submission.save()
        self._update_user_statues_handler()

        # process submission in the redis
        process_submission_in_redis()
    
    def _update_user_statues_handler(self):
        with transaction.atomic():
            self.problem.submission_number += 1
            if self.submission.result == JudgeStatus.ACCEPTED:
                self.problem.ac_number += 1
            self.problem.save()
            try:
                user = User.objects.get(id=self.submission.user_id)
                user_profile = UserProfile.objects.get(user=user)
            except Exception as e:
                logger.exception(e)
                return
            user_profile.submission_number += 1
            if self.submission.result == JudgeStatus.ACCEPTED:
                user_profile.accepted_number += 1
                user_profile.accepted_problems.add(self.problem.id)
            user_profile.save()


class BattleJudgeHandler(BaseHandler):
    def __init__(self, data):
        super().__init__()
        self.user_id = data['user_id']
        self.problem_id = data['problem_id']
        self.battle_id = data['battle_id']
        self.code = data['code']
        self.language = data['language']
        self.problem = Problem.objects.get(id=self.problem_id)
        self.submission = Submission.objects.create(
            pro=self.problem,
            user_id=self.user_id,
            code=self.code,
            language=self.language,
            battle_id=self.battle_id
        )

    def _static_info_handler(self, data):
        info = {}
        info['time_cost'] = max([x['cpu_time'] for x in data])
        info['memory_cost'] = max([x['memory'] for x in data])
        self.submission.static_info = info

    def judge(self):
        language = self.language
        config = list(filter(lambda item: language == item["name"], languages))[0]
        code = self.code
        data = {
            "src": code,
            "language_config": config['config'],
            "max_cpu_time": self.problem.time_limit,
            "max_memory": 1024 * 1024 * self.problem.memory_limit,
            "test_case_id": str(self.problem.id),
            "output": False,
        }

        Submission.objects.filter(id=self.submission.id).update(result=JudgeStatus.JUDGING)
        resp = self._request(data)
        if not resp:
            Submission.objects.filter(id=self.submission.id).update(result=JudgeStatus.SYSTEM_ERROR)
            resp_data = {'code': 0, 'msg': 'submit success', 'data': {
                'result': JudgeStatus.SYSTEM_ERROR
            }}
            return resp_data

        if 'code' in resp.keys():
            # put this submission into the redis
            # submit_data = {"submission_id": self.submission.id, "problem_id": self.problem.id}
            # Cache = django_redis.get_redis_connection()
            # Cache.lpush("waiting_queue", json.dumps(submit_data))
            resp_data = {'code': -999, 'msg': 'Judge Server Error', 'data': {}}
            return resp_data
        elif resp['err']:
            self.submission.result = JudgeStatus.COMPILE_ERROR
            info = {'err_info': resp['data']}
            self.submission.static_info = info
        else:
            resp["data"].sort(key=lambda x: int(x["test_case"]))
            self.submission.info = resp
            self._static_info_handler(resp['data'])
            error_test_case = list(filter(lambda case: case["result"] != 0, resp["data"]))
            if not error_test_case:
                self.submission.result = JudgeStatus.ACCEPTED
            else:
                self.submission.result = error_test_case[0]["result"]

        self.submission.save()
        resp_data = {'code': 0, 'msg': 'submit success', 'data': {
            'result': self.submission.result,
            'info': self.submission.static_info,
            'create_time': self.submission.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            'language': self.submission.language,
            'code': self.submission.code
        }}
        return resp_data