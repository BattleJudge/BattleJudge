from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from conf.project_conf import AVATAR_URI_PREFIX
from django_mysql.models import SetTextField


class UserType(object):
    REGULAR_USER = "Regular User"
    ADMIN_USER = "Admin User"


class UserManager(BaseUserManager):
    def _create_user(self, username, password, **kwargs):
        if not username:
            raise ValueError("request username")
        if not password:
            raise ValueError("request password")
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()

        user_profile = UserProfile.objects.create(user=user)
        user_profile.nickname = username
        user_profile.save()
        return user

    def create_user(self, username, password, **kwargs):
        return self._create_user(username, password, **kwargs)

    def create_superuser(self, username, password, **kwargs):
        kwargs['user_type'] = UserType.ADMIN_USER
        kwargs['is_superuser'] = True
        return self._create_user(username, password, **kwargs)


class User(AbstractUser):
    # base info
    username = models.CharField(max_length=150, unique=True, null=False, blank=False)
    password = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False,default='')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    user_type = models.TextField(default=UserType.REGULAR_USER)

    # reset pwd need
    reset_password_token = models.TextField(null=True)
    reset_password_token_expire_time = models.DateTimeField(null=True)

    # reset email need
    reset_email_token = models.TextField(null=True)
    reset_email_token_expire_time = models.DateTimeField(null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def is_admin(self):
        return self.user_type == UserType.ADMIN_USER

    class Meta:
        db_table = "user"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.TextField(default=f"{AVATAR_URI_PREFIX}/default.png")
    nickname = models.CharField(unique=True, null=False, blank=False, max_length=32)
    motto = models.TextField(null=False, blank=True, default='')
    submission_number = models.IntegerField(default=0)
    accepted_number = models.IntegerField(default=0)
    accepted_problems = SetTextField(
        base_field=models.IntegerField()
    )
    battle_score = models.IntegerField(default=1500)
    battle_win = models.IntegerField(default=0)
    battle_lose = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def add_submission_number(self):
        self.submission_number = models.F("submission_number") + 1
        self.save()

    def add_accepted_problem_number(self, problem_id):
        self.accepted_number = models.F("accepted_number") + 1
        self.accepted_problems.add(problem_id)
        self.save()

    def add_battle_score(self, val):
        self.battle_score = models.F("battle_score") + int(val)
        self.save()

    class Meta:
        db_table = "user_profile"
