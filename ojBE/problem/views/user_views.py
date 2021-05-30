import numbers
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
from ..models import ProblemTag, Problem, Solution
from ..serializers import (UserGetProblemInfoSerializer, UserGetProblemInfoByIDSerializer, 
                            UserGetProblemListSerializer, UserGetProblemSolutionInfoSerializer,
                            UserGetProblemSolutionListSerializer, UserAddProblemSolutionSerializer, 
                            UserUpdateProblemSolutionSerializer, )
from ..pagination import (UserGetProblemListPagination, UserGetProblemSolutionListPagination,)

logger = logging.getLogger(__name__)

class ProblemListAPI(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        resp_data = {}
        data = None
        if ('id' in request.GET):
            id = request.GET.get('id')
            # id not number
            if not id.isdigit():
                resp_data['code'] = -1
                resp_data['msg'] = "request data error"
                resp_data['data'] = {}
                return Response(data=resp_data)
            
            id = int(id)

            # id problem not exist
            try:
                pro = Problem.objects.get(id=id)
            except Problem.DoesNotExist:
                resp_data['code'] = -2
                resp_data['msg'] = f"{id} problem does not exist"
                resp_data['data'] = {}
                return Response(data=resp_data)
            
            # user no auth
            if not pro.visible:
                try:
                    user, token = get_user_and_token_by_jwt_request(request)
                    if user.user_type != UserType.ADMIN_USER:
                        resp_data['code'] = -3
                        resp_data['msg'] = "no authority"
                        resp_data['data'] = {}
                        return Response(data=resp_data)
                except Exception as e:
                    pass

            data = []
            data.append(UserGetProblemListSerializer(pro).data)
            resp_data['total'] = 1
        else:
            problem_list = Problem.objects.filter(visible=True).order_by('id')
            page_data = UserGetProblemListPagination().paginate_queryset(problem_list, request, self)
            data = UserGetProblemListSerializer(page_data, many=True).data
            resp_data['total'] = Problem.objects.filter(visible=True).count()

        for v in data:
            if v['submission_number'] == 0:
                v['ac_rate'] = 0.00
            else:
                v['ac_rate'] = round(v['ac_number'] / v['submission_number'], 2)
        resp_data['data'] = data
        try:
            user, token = get_user_and_token_by_jwt_request(request)
            user_profile = UserProfile.objects.get(user=user)
            for v in data:
                if v['id'] in user_profile.accepted_problems:
                    v['ac'] = True
                else:
                    v['ac'] = False
        except Exception as e:
            logger.exception(e)
            pass
        return Response(data=resp_data)


class ProblemAPI(APIView):

    permission_classes = [AllowAny]

    def get(self, request):
        resp_data = {'code': 0, 'msg': 'success', 'data': {}}

        serializer = UserGetProblemInfoByIDSerializer(data=request.GET)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(data=resp_data)

        id = serializer.data['id']
        try:
            pro = Problem.objects.get(id=id)
        except Problem.DoesNotExist:
            resp_data['code'] = -2
            resp_data['msg'] = f"{id} problem does not exist"
            return Response(data=resp_data)

        if not pro.visible:
            try:
                user, token = get_user_and_token_by_jwt_request(request)
                if user.user_type != UserType.ADMIN_USER:
                    resp_data['code'] = -3
                    resp_data['msg'] = 'no authority'
                    return Response(data=resp_data)
            except Exception as e:
                resp_data['code'] = -3
                resp_data['msg'] = 'no authority'
                return Response(data=resp_data)

        data = UserGetProblemInfoSerializer(pro).data
        try:
            data['created_by'] = UserProfile.objects.get(user=pro.create_by).nickname
        except Exception as e:
            data['created_by'] = 'root'

        resp_data['data'] = data
        return Response(data=resp_data)


class SolutionListAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        resp_data = {}

        serializer = UserGetProblemSolutionListSerializer(data=request.GET)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            resp_data['data'] = {}
            return Response(data=resp_data)

        pro_id = serializer.data['pro_id']
        solution_list = Solution.objects.filter(pro_id=pro_id).order_by('create_time')
        page_data = UserGetProblemSolutionListPagination().paginate_queryset(solution_list, request, self)
        data = UserGetProblemSolutionInfoSerializer(page_data, many=True).data
        for v in data:
            try:
                user = User.objects.get(username=v['author'])
                user_profile = UserProfile.objects.get(user=user)
                v['author'] = user_profile.nickname
            except Exception as e:
                v['author'] = 'root'

        resp_data['total'] = Solution.objects.filter(pro_id=pro_id).count()
        resp_data['data'] = data
        return Response(data=resp_data)


class SolutionAPI(APIView):
    
    permission_classes = [IsAuthenticated]

    def put(self, request):
        resp_data = {'code': 0, 'msg': 'success', 'data': {}}

        serializer = UserAddProblemSolutionSerializer(data=request.data)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(data=resp_data)
        
        pro_id = serializer.data['pro_id']
        if not Problem.objects.filter(id=pro_id).exists():
            resp_data['code'] = -2
            resp_data['msg'] = f"{pro_id} problem does not exist"
            return Response(data=resp_data)
        user, token = get_user_and_token_by_jwt_request(request)
        solution = Solution.objects.create(pro_id=pro_id, content=serializer.data['content'], author=user)
        solution.save()

        resp_data['data'] = UserGetProblemSolutionInfoSerializer(solution).data
        return Response(data=resp_data)

    def post(self, request):
        resp_data = {'code': 0, 'msg': 'success', 'data': {}}

        serializer = UserUpdateProblemSolutionSerializer(data=request.data)
        if not serializer.is_valid():
            resp_data['code'] = -1
            resp_data['msg'] = 'request data error'
            return Response(data=resp_data)

        try:
            solution = Solution.objects.get(id=serializer.data['id'])
        except Solution.DoesNotExist:
            resp_data['code'] = -2
            resp_data['msg'] = f"{serializer.data['id']} solution does not exist"
            return Response(data=resp_data)

        user, token = get_user_and_token_by_jwt_request(request)
        if not (solution.author == user or user.user_type == UserType.ADMIN_USER):
            resp_data['code'] = -3
            resp_data['msg'] = 'no authority'
            return Response(data=resp_data)

        solution.content = serializer.data['content']
        solution.save()
        resp_data['data'] = UserGetProblemSolutionInfoSerializer(solution).data
        return Response(data=resp_data)