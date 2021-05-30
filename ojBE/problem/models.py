from django.db import models
from django_mysql.models import JSONField, SetTextField
from account.models import User


class ProblemTag(models.Model):
    name = models.TextField()

    class Meta:
        db_table = "problem_tag"


class Problem(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.TextField()
    description = models.TextField()
    input_description = models.TextField()
    output_description = models.TextField()
    # [{"input": "hello", "output": "world"}]
    samples = JSONField()
    hint = models.TextField(null=True)
    problem_source = models.TextField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    time_limit = models.IntegerField() # ms
    memory_limit = models.IntegerField() # MB
    tags = SetTextField(
        base_field = models.CharField(max_length=150)
    )
    visible = models.BooleanField(default=True)
    in_battle_set = models.BooleanField(default=False)
    difficulty = models.TextField()
    submission_number = models.BigIntegerField(default=0)
    ac_number = models.BigIntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(null=True)

    class Meta:
        db_table = "problem"
        ordering = ("create_time", )

    def add_submission_number(self):
        self.submission_number = models.F("submission_number") + 1
        self.save()

    def add_ac_number(self):
        self.ac_number = models.F("ac_number") + 1
        self.save()


class Solution(models.Model):
    id = models.BigAutoField(primary_key=True)
    pro_id = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "problem_solution"