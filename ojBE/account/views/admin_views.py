import sys
sys.path.append('../../')
from ..serializers import (AdminManagerUserInfoSerializer, AdminUpdateUserInfoSerializer, 
                            AdminGetUserInfoByUsernameSerializer, AdminAddUserSerializer,
                            AdminDeleteUserSerializer, )
from ..models import User, UserProfile, UserType
from ..permission import IsAdminUserPermission
from ..pagination import AdminManagerUserInfoPagination
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response


class AdminGetUserInfoList(APIView):

    permission_classes = [IsAuthenticated, IsAdminUserPermission]

    def get(self, request):
        user_profile_list = UserProfile.objects.all().order_by('user_id')

        page_data = AdminManagerUserInfoPagination().paginate_queryset(user_profile_list, request, self)
        resp_data = AdminManagerUserInfoSerializer(page_data, many=True)

        resp = {}
        resp['data'] = resp_data.data
        resp['total'] = UserProfile.objects.all().count()
        return Response(resp)


class AdminUpdateUserInfo(APIView):

    permission_classes = [IsAuthenticated, IsAdminUserPermission]

    def post(self, request):
        resp_data = {'code': 0, 'msg': 'success', 'data': {}}

        serializer = AdminUpdateUserInfoSerializer(data=request.data)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(resp_data)

        username = serializer.data['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            resp_data['code'] = -2
            resp_data['msg'] = f"{username} does not exist"
            return Response(data=resp_data)

        resp_data['data']['id'] = user.pk
        resp_data['data']['username'] = username
        user_profile = UserProfile.objects.get(user=user)

        if user_profile.nickname != serializer.data['nickname']:
            nickname = serializer.data['nickname']
            if UserProfile.objects.filter(nickname=nickname).exists():
                resp_data['data']['nickname'] = '-1'
            else:
                user_profile.nickname = nickname
                user_profile.save()
                resp_data['data']['nickname'] = nickname
        else:
            resp_data['data']['nickname'] = serializer.data['nickname']

        if 'password' in serializer.data:
            user.set_password(serializer.data['password'])

        if user.email != serializer.data['email']:
            email = serializer.data['email']
            if User.objects.filter(email=email).exists():
                resp_data['data']['email'] = '-1'
            else:
                resp_data['data']['email'] = email
                user.email = email
        else:
            resp_data['data']['email'] = serializer.data['email']

        user_type = serializer.data['user_type']
        if user_type == UserType.ADMIN_USER:
            user.user_type = UserType.ADMIN_USER
            user.is_superuser = True
            resp_data['data']['user_type'] = UserType.ADMIN_USER
        elif user_type == UserType.REGULAR_USER:
            user.user_type = UserType.REGULAR_USER
            user.is_superuser = False
            resp_data['data']['user_type'] = UserType.REGULAR_USER
        else:
            resp_data['data']['user_type'] = '-1'

        user.save()
        return Response(data=resp_data)


class AdminGetUserInfoByUsername(APIView):
    
    permission_classes = [IsAuthenticated, IsAdminUserPermission]

    def get(self, request):
        resp_data = {'code': 0, 'msg': 'success', 'data': {}}

        serializer = AdminGetUserInfoByUsernameSerializer(data=request.GET)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(resp_data)
        username = request.GET.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            resp_data['code'] = -2
            resp_data['msg'] = f"{username} does not exist"
            return Response(data=resp_data)

        resp_data['data']['id'] = user.pk
        resp_data['data']['username'] = user.username
        resp_data['data']['nickname'] = UserProfile.objects.get(user=user).nickname
        resp_data['data']['email'] = user.email
        resp_data['data']['user_type'] = user.user_type

        return Response(data=resp_data)


class AdminManagerUser(APIView):

    permission_classes = [IsAuthenticated, IsAdminUserPermission]

    def post(self, request):
        resp_data = {'code': 0, 'msg': 'success', 'data': {}}

        serializer = AdminAddUserSerializer(data=request.data)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(resp_data)

        data = request.data
        username = data['username']
        nickname = data['nickname']
        password = data['password']
        email = data['email']
        user_type = data['user_type']

        if User.objects.filter(username=username).exists():
            resp_data['code'] = 1
            resp_data['msg'] = f"{username} does exist"
            return Response(data=resp_data)

        if UserProfile.objects.filter(nickname=nickname).exists():
            resp_data['code'] = 2
            resp_data['msg'] = f"{nickname} does exist"
            return Response(data=resp_data)

        if User.objects.filter(email=email).exists():
            resp_data['code'] = 3
            resp_data['msg'] = f"{email} does exist"
            return Response(data=resp_data)

        if not (user_type == UserType.REGULAR_USER or user_type == UserType.ADMIN_USER):
            user_type = UserType.REGULAR_USER

        is_superuser = False
        if user_type == UserType.ADMIN_USER:
            is_superuser = True
        user = User.objects.create(username=username, email=email, user_type=user_type, is_superuser=is_superuser)
        user.set_password(password)
        user.save()

        user_profile = UserProfile.objects.create(user=user)
        user_profile.nickname = nickname
        user_profile.save()

        return Response(data=resp_data)

    def delete(self, request):
        resp_data = {'code': 0, 'msg': 'success', 'data': {}}

        serializer = AdminDeleteUserSerializer(data=request.GET)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(resp_data)

        username = serializer.data['username']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            resp_data['code'] = -2
            resp_data['msg'] = f"{username} does not exist"
            return Response(resp_data)

        user_profile = UserProfile.objects.get(user=user)
        user_profile.delete()
        user.delete()

        return Response(data=resp_data)