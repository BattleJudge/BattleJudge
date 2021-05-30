import sys
import os
import json
sys.path.append("../../")
from account.models import User, UserProfile
from account.permission import IsAdminUserPermission
from django.core import serializers
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from utils.api import get_user_and_token_by_jwt_request
from conf.project_conf import JUDGE_SERVER_TEST_CASE_URL
from ..models import ProblemTag, Problem
from ..serializers import (AdminAddProblemSerializer, AdminAddTagSerializer,
                            AdminGetProblemListSerializer, AdminUpdateProblemSerializer, 
                            UploadFileSerializer, AdminGetProblemByIDSerializer, 
                            ReturnAdminGetProbelmByIDSerializer, )
from ..pagination import (AdminGetProblemListPagination, )
from ..tasks import send_test_case_to_judge


class ProblemListAPI(APIView):
    
    permission_classes = [IsAuthenticated, IsAdminUserPermission]

    def get(self, request):
        problem_list = Problem.objects.all().order_by('id')
        page_data = AdminGetProblemListPagination().paginate_queryset(problem_list, request, self)
        data = AdminGetProblemListSerializer(page_data, many=True)
        data = data.data
        for k in data:
            try:
                user = User.objects.get(username=k['created_by'])
                k['created_by'] = UserProfile.objects.get(user=user).nickname
            except Exception as e:
                pass
        resp_data = {}
        resp_data['total'] = Problem.objects.all().count()
        resp_data['data'] = data
        return Response(data=resp_data)


class ProblemAPI(APIView):

    permission_classes = [IsAuthenticated, IsAdminUserPermission]

    def get(self, request):
        resp_data = {'code': 0, 'msg': 'success', 'data': {}}
        serializer = AdminGetProblemByIDSerializer(data=request.GET)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(data=resp_data)

        data = serializer.data
        id = data['id']

        try:
            pro = Problem.objects.get(id=id)
        except Problem.DoesNotExist:
            resp_data['code'] = -2
            resp_data['msg'] = f"{id} problem does not exist"
            return Response(data=resp_data)

        data = ReturnAdminGetProbelmByIDSerializer(pro).data
        try:
            user = User.objects.get(username=data['created_by'])
            data['created_by'] = UserProfile.objects.get(user=user).nickname
        except Exception as e:
            pass

        resp_data['data'] = data
        return Response(data=resp_data)

    def put(self, request):
        resp_data = {'code': 0, 'msg': 'success', 'data': {}}
        serializer = AdminAddProblemSerializer(data=request.data)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(data=resp_data)

        user, token = get_user_and_token_by_jwt_request(request)
        data = serializer.data
        data['created_by'] = user
        tags = data.pop('tags')
        try:
            pro = Problem.objects.create(**data)
        except Exception as e:
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(data=resp_data)

        for item in tags:
            if not ProblemTag.objects.filter(name=item).exists():
                tag = ProblemTag.objects.create(name=item)
                tag.save()
            pro.tags.add(item)
        pro.last_update_time = now()
        pro.save()

        pro_data = AdminAddProblemSerializer(pro)
        resp_data['data'] = pro_data.data
        resp_data['data']['id'] = pro.pk
        resp_data['data']['created_by'] = UserProfile.objects.get(user=user).nickname
        return Response(data=resp_data)

    def post(self, request):
        resp_data = {'code': 0, 'msg': 'success', 'data': {}}

        serializer = AdminUpdateProblemSerializer(data=request.data)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(data=resp_data)
        user, token = get_user_and_token_by_jwt_request(request)
        data = serializer.data
        try:
            pro = Problem.objects.get(id=data['id'])
        except Problem.DoesNotExist:
            resp_data['code'] = -2
            resp_data['msg'] = f"{data['id']} problem does not exist"
            return Response(data=resp_data)

        tags = data.pop('tags')

        for k, v in data.items():
            setattr(pro, k, v)
        
        pro.tags.clear()
        for item in tags:
            if not ProblemTag.objects.filter(name=item).exists():
                tag = ProblemTag.objects.create(name=item)
                tag.save()
            pro.tags.add(item)
        pro.last_update_time = now()
        pro.save()
        pro_data = AdminUpdateProblemSerializer(pro)
        resp_data['data'] = pro_data.data
        resp_data['data']['created_by'] = UserProfile.objects.get(user=user).nickname
        return Response(data=resp_data)


class ProblemTagAPI(APIView):

    permission_classes = [IsAuthenticated, IsAdminUserPermission]

    def get(self, request):
        resp_data = {'code': 0, 'msg': 'success', 'data':{}}
        query_set = ProblemTag.objects.all()
        resp_data['data']['tags'] = serializers.serialize('json', query_set)
        return Response(data=resp_data)

    def post(self, request):
        resp_data = {'code': 0, 'msg': 'success', 'data':{}}

        serializer = AdminAddTagSerializer(data=request.data)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(data=resp_data)

        tag = serializer.data['tag']
        if ProblemTag.objects.filter(name=tag).exists():
            resp_data['code'] = -2
            resp_data['msg'] = f"{tag} exist"
            return Response(data=resp_data)
        
        new_tag = ProblemTag.objects.create(name=tag)
        new_tag.save()

        return Response(data=resp_data)


class ProblemTestCaseAPI(APIView):

    permission_classes = [IsAuthenticated, IsAdminUserPermission]

    def post(self, request):
        resp_data = {'code': 0, 'msg': 'success', 'data': {}}

        serializer = UploadFileSerializer(request.POST, request.FILES)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(data=resp_data)

        test_case = request.FILES['file']
        test_case_suf = os.path.splitext(test_case.name)[-1].lower()
        if test_case_suf != '.zip':
            resp_data['code'] = -2
            resp_data['msg'] = f"{test_case_suf} unsupport"
            return Response(data=resp_data)

        pro_id = serializer.data['id']
        test_case_name = str(pro_id) + '.zip'
        with open(os.path.join("./data/test_case/", test_case_name), "wb") as f:
            for chunk in test_case:
                f.write(chunk)

        file = {'file': open(os.path.join("./data/test_case", test_case_name), "rb")}
        data = {'problem_id': pro_id}
        pack = send_test_case_to_judge(JUDGE_SERVER_TEST_CASE_URL, data, file)
        resp_data = pack
        return Response(data=resp_data)