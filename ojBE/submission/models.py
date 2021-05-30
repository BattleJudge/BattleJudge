from django.db import models
from django_mysql.models import JSONField
from problem.models import Problem


class JudgeStatus(object):
    COMPILE_ERROR = -2
    WRONG_ANSWER = -1
    ACCEPTED = 0
    CPU_TIME_LIMIT_EXCEEDED = 1
    REAL_TIME_LIMIT_EXCEEDED = 2
    MEMORY_LIMIT_EXCEEDED = 3
    RUNTIME_ERROR = 4
    SYSTEM_ERROR = 5
    PENDING = 6
    JUDGING = 7
    PARTIALLY_ACCEPTED = 8


class Submission(models.Model):
    id = models.BigAutoField(primary_key=True)
    pro = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user_id = models.IntegerField(db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)
    code = models.TextField()
    result = models.IntegerField(db_index=True, default=JudgeStatus.PENDING)
    # Judge 返回的信息
    info = JSONField()
    # 用时, 内存
    static_info = JSONField()
    language = models.TextField()
    battle_id = models.IntegerField(default=None)

    class Meta:
        db_table = "submission"