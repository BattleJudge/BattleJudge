import logging
import sys
sys.path.append("../../")
from account.models import User, UserProfile, UserType
from account.permission import IsAdminUserPermission
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from utils.api import get_user_and_token_by_jwt_request
from problem.models import Problem
from judge.tasks import judge
from ..models import Submission
from ..serializers import (UserSubmitCodeSerializer, UserGetSubmissionResultSerializer, 
                            ReturnUserGetSubmissionResultSerializer, UserGetSubmissionList, 
                            ReturnUserGetSubmissionList, )
from ..pagination import UserGetSubmissionListPagination


logger = logging.getLogger(__name__)

class SubmissionAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        resp_data = {'code': 0, 'msg': 'success', 'data': {}}

        serializer = UserGetSubmissionResultSerializer(data=request.GET)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(data=resp_data)

        submission_id = serializer.data['submission_id']
        try:
            submission = Submission.objects.get(id=submission_id)
        except Submission.DoesNotExist:
            resp_data['code'] = -2
            resp_data['msg'] = f"{submission_id} submission does not exist"
            return Response(data=resp_data)

        user, token = get_user_and_token_by_jwt_request(request)
        if (user.id != submission.user_id) and (user.user_type != UserType.ADMIN_USER):
            resp_data['code'] = -3
            resp_data['msg'] = 'no authority'
            return Response(data=resp_data)

        data = ReturnUserGetSubmissionResultSerializer(submission).data
        resp_data['data'] = data
        return Response(data=resp_data)

    def post(self, request):
        resp_data = {'code': 0, 'msg': 'success', 'data': {}}

        serializer = UserSubmitCodeSerializer(data=request.data)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(data=resp_data)
        
        pro_id = serializer.data['pro_id']
        try:
            pro = Problem.objects.get(id=pro_id)
        except Problem.DoesNotExist:
            resp_data['code'] = -2
            resp_data['msg'] = f"{pro_id} problem does not exist"
            return Response(data=resp_data)

        user, token = get_user_and_token_by_jwt_request(request)

        if (user.user_type == UserType.REGULAR_USER) and (not pro.visible):
            resp_data['code'] = -3
            resp_data['msg'] = 'no authority'
            return Response(data=resp_data)

        submission = Submission.objects.create(
                                                pro=pro,
                                                user_id=user.pk,
                                                code=serializer.data['code'],
                                                language=serializer.data['language'],
                                                battle_id=0
                                                )
        submission.save()
        judge.delay(submission.id, pro_id)
        resp_data['data']['submission_id'] = submission.id
        return Response(data=resp_data)


class SubmissionListAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserGetSubmissionList(data=request.GET)
        if not serializer.is_valid():
            resp_data = {'code': 0, 'msg': 'success', 'data': {}}
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(data=resp_data)
        pro_id = serializer.data['pro_id']
        try:
            pro = Problem.objects.get(id=pro_id)
        except Problem.DoesNotExist:
            resp_data['code'] = -2
            resp_data['msg'] = f"{pro_id} problem does not exist"
            return Response(data=resp_data)

        user, token = get_user_and_token_by_jwt_request(request)

        submission_list = Submission.objects.filter(pro=pro, user_id=user.id, battle_id=0).order_by('-create_time')
        page_data = UserGetSubmissionListPagination().paginate_queryset(submission_list, request, self)
        data = ReturnUserGetSubmissionList(page_data, many=True).data
        resp_data = {}
        resp_data['data'] = data
        resp_data['total'] = Submission.objects.filter(pro=pro, user_id=user.id, battle_id=0).count()
        return Response(data=resp_data)
