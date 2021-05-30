import os
import sys
import time
from datetime import timedelta
sys.path.append('../../')
from django.contrib import auth
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny, IsAuthenticated, )
from rest_framework_simplejwt.tokens import RefreshToken
from ..serializers import (UserRegisterSerializer, UserLoginSerializer,
                            ImageUploadForm, UserChangePasswordSerializer,
                            UserResetPasswordSerializer, GetUserResetEmailTokenSerializer,
                            UserResetEmailSerializer, GetUserResetPasswordTokenSerializer,
                            UpdateUserProfleSerializer, )
from ..models import (User, UserProfile, )
from ..backend import (LoginBackend, )
from conf.project_conf import (AVATAR_MAX_SIZE, AVATAR_FILE_PATH, AVATAR_SUPPORT_TYPE, AVATAR_URI_PREFIX, )
from utils.api import (rand_str, get_user_and_token_by_jwt_request, async_send_email, )


class UserRegisterView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        resp_data = {'code': 0, 'msg': 'success', 'data': {}}

        serializer = UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(data=resp_data)

        data = request.data
        username = data['username']
        password = data['password']
        nickname = data['nickname']
        email = email = data['email']
        if User.objects.filter(username=username).exists():
            resp_data['code'] = 1
            resp_data['msg'] = 'username exist'
            return Response(data=resp_data)
        if User.objects.filter(email=email).exists():
            resp_data['code'] = 2
            resp_data['msg'] = 'email exist'
            return Response(data=resp_data)
        if UserProfile.objects.filter(nickname=nickname).exists():
            resp_data['code'] = 3
            resp_data['msg'] = 'nicename exist'
            return Response(data=resp_data)
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        
        user_profile = UserProfile.objects.create(user=user)
        user_profile.nickname = nickname
        user_profile.save()

        return Response(data=resp_data)

        
class UserLoginView(APIView):

    authentication_classes = [LoginBackend, ]
    permission_classes = [AllowAny]

    def post(self, request):
        resp_data = {'code': 0, 'msg': "success", 'data': {}}

        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(data=resp_data)

        data = request.data
        username = data['username']
        password = data['password']

        user = auth.authenticate(username=username, password=password)

        if user:
            jwt_refresh = RefreshToken.for_user(user)
            user_profile = UserProfile.objects.get(user=user)
            resp_data['data']['access'] = str(jwt_refresh.access_token)
            resp_data['data']['refresh'] = str(jwt_refresh)
            resp_data['data']['user_type'] = str(user.user_type)
            resp_data['data']['id'] = int(user.pk)
            resp_data['data']['avatar'] = str(user_profile.avatar)
            return Response(data=resp_data)
        else:
            resp_data['code'] = 1
            resp_data['msg'] = 'username or password error'
            return Response(data=resp_data)


class UserUploadAvatar(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        resp_data = {'code': '0', 'msg': 'success', 'data': {}}
        form = ImageUploadForm(request.POST, request.FILES)
        if not form.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(data=resp_data)

        avatar = form.cleaned_data['image']

        if avatar.size > AVATAR_MAX_SIZE:
            resp_data['code'] = 1
            resp_data['msg'] = 'avatar size too large'
            return Response(data=resp_data)

        avatar_suf = os.path.splitext(avatar.name)[-1].lower()
        if avatar_suf not in AVATAR_SUPPORT_TYPE:
            resp_data['code'] = 2
            resp_data['msg'] = 'unsupport file format'
            return Response(data=resp_data)

        avatar_name = rand_str() + str(int(time.time())) + avatar_suf

        with open(os.path.join(AVATAR_FILE_PATH, avatar_name), "wb") as img:
            for chunk in avatar:
                img.write(chunk)

        user, token = get_user_and_token_by_jwt_request(request)
        user_profile = UserProfile.objects.get(user=user)
        user_profile.avatar = f"{AVATAR_URI_PREFIX}/{avatar_name}"
        user_profile.save()

        resp_data['data']['avatar'] = user_profile.avatar
        return Response(data=resp_data)


class UserChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        resp_data = {'code': '0', 'msg': 'success', 'data': {}}

        serializer = UserChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(data=resp_data)

        user, token = get_user_and_token_by_jwt_request(request)
        data = request.data
        old_password = data['old_password']
        new_password = data['new_password']
        if not auth.hashers.check_password(old_password, user.password):
            resp_data['code'] = 1
            resp_data['msg'] = 'old_password error'
            return Response(data=resp_data)

        user.set_password(new_password)
        user.save()

        return Response(data=resp_data)


class GetUserResetPasswordToken(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        resp_data = {'code':0, 'msg':'success', 'data':{}}
        serializer = GetUserResetPasswordTokenSerializer(data=request.GET)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(data=resp_data)
        
        try:
            user = User.objects.get(username=request.GET.get('username'))
        except User.DoesNotExist:
            resp_data['code'] = -2
            resp_data['msg'] = f"{request.GET.get('username')} does not exist"
            return Response(data=resp_data)

        user_email = user.email
        user_reset_token = rand_str(len=6, type='num')
        user.reset_password_token = user_reset_token
        user.reset_password_token_expire_time = now() + timedelta(minutes=20)
        user.save()
        nickname = UserProfile.objects.get(user=user).nickname
        message = f"Hello {nickname}:\nYour reset password token is {user_reset_token}, the token is valid for 20 minutes."
        async_send_email.delay(subject='Reset your password', message=message, recipient_list=[str(user.email)])
        resp_data['data']['email_to'] = user.email
        return Response(data=resp_data)


class UserResetPassword(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        resp_data = {'code': 0, 'msg': 'success', 'data': {}}

        serializer = UserResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(data=resp_data)

        data = request.data
        username = data['username']
        reset_token = data['token']
        new_password = data['new_password']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            resp_data['code'] = -2
            resp_data['msg'] = f"{username} does not exist"
            return Response(data=resp_data)

        if (user.reset_password_token is None) or (not (user.reset_password_token == reset_token)):
            resp_data['code'] = 1
            resp_data['msg'] = 'reset password token error'
            return Response(data=resp_data)

        if user.reset_password_token_expire_time < now():
            resp_data['code'] = 2
            resp_data['msg'] = 'reset password token invalid'
            return Response(data=resp_data)

        user.set_password(new_password)
        user.reset_password_token = None
        user.save()

        return Response(data=resp_data)


class GetUserResetEmailToken(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        resp_data = {'code': 0, 'msg': 'success', 'data': {}}

        serializer = GetUserResetEmailTokenSerializer(data=request.GET)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(data=resp_data)

        data = request.data
        new_email = request.GET.get('new_email')
        op_type = request.GET.get('op_type')        

        user, token = get_user_and_token_by_jwt_request(request)
        if op_type == 'bound' and len(user.email) > 0:
            resp_data['code'] = 1
            resp_data['msg'] = 'the user has already bound the mailbox'
            resp_data['data']['email'] = user.email
            return Response(data=resp_data)

        try:
            user = User.objects.get(email=new_email)
            resp_data['code'] = 2
            resp_data['msg'] = 'the new email is bound by someone else'
            return Response(data=resp_data)
        except User.DoesNotExist:
            pass

        email_to = ''
        if op_type == 'bound':
            email_to = new_email
        elif op_type == 'reset':
            email_to = user.email
        else:
            resp_data['code'] = -2
            resp_data['msg'] = 'operation type error'
            return Response(data=resp_data)

        user_reset_token = rand_str(len=6, type='num')
        user.reset_email_token = user_reset_token
        user.reset_email_token_expire_time = now() + timedelta(minutes=20)
        user.save()
        nickname = UserProfile.objects.get(user=user).nickname
        message = f"Hello {nickname}:\nYour {op_type} email token is {user_reset_token}, the token is valid for 20 minutes."
        async_send_email.delay(subject=f"{op_type.capitalize()} your email", message=message, recipient_list=[str(email_to)])
        resp_data['data']['email_to'] = email_to
        return Response(data=resp_data)


class UserResetEmail(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        resp_data = {'code': 0, 'msg': 'success', 'data': {}}

        serializer = UserResetEmailSerializer(data=request.data)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(data=resp_data)

        data = request.data
        reset_token = data['token']
        new_email = data['new_email']

        user, token = get_user_and_token_by_jwt_request(request)
        if (user.reset_email_token is None) or (not (user.reset_email_token == reset_token)):
            resp_data['code'] = 1
            resp_data['msg'] = 'reset email token error'
            return Response(data=resp_data)

        if user.reset_email_token_expire_time < now():
            resp_data['code'] = 2
            resp_data['msg'] = 'reset email token invalid'
            return Response(data=resp_data)

        user.email = new_email
        user.reset_email_token = None
        user.save()
        return Response(data=resp_data)


class GetUsereProfile(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        resp_data = {'code': 0, 'msg': 'success', 'data': {}}

        user, token = get_user_and_token_by_jwt_request(request)

        user_profile = UserProfile.objects.get(user=user)

        resp_data['data']['avatar'] = user_profile.avatar
        resp_data['data']['username'] = user.username
        resp_data['data']['nickname'] = user_profile.nickname
        resp_data['data']['motto'] = user_profile.motto
        resp_data['data']['email'] = user.email
        resp_data['data']['submission_number'] = user_profile.submission_number
        resp_data['data']['accepted_number'] = user_profile.accepted_number
        return Response(data=resp_data)

    def put(self, request):
        resp_data = {'code': 0, 'msg': 'success', 'data': {}}

        serializer = UpdateUserProfleSerializer(data=request.data)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(data=resp_data)

        user, token = get_user_and_token_by_jwt_request(request)
        user_profile = UserProfile.objects.get(user=user)
        for k, v in serializer.data.items():
            setattr(user_profile, k, v)
        user_profile.save()

        resp_data['data']['avatar'] = user_profile.avatar
        resp_data['data']['username'] = user.username
        resp_data['data']['nickname'] = user_profile.nickname
        resp_data['data']['motto'] = user_profile.motto
        resp_data['data']['email'] = user.email
        resp_data['data']['submission_number'] = user_profile.submission_number
        resp_data['data']['accepted_number'] = user_profile.accepted_number
        return Response(data=resp_data)
