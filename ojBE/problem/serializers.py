from django import forms
from rest_framework import serializers
from .models import Problem


class AddSampleSerializer(serializers.Serializer):
    input = serializers.CharField()
    output = serializers.CharField()


class AdminAddProblemSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    input_description = serializers.CharField(required=True)
    output_description = serializers.CharField(required=True)
    samples = serializers.ListField(required=True, child=AddSampleSerializer(), allow_empty=False)
    hint = serializers.CharField(required=True)
    problem_source = serializers.CharField(required=True)
    time_limit = serializers.IntegerField(required=True)
    memory_limit = serializers.IntegerField(required=True)
    tags = serializers.ListField(required=True, child=serializers.CharField(max_length=150), allow_empty=True)
    visible = serializers.BooleanField(required=True)
    in_battle_set = serializers.BooleanField(required=True)
    difficulty = serializers.CharField(required=True)


class AdminUpdateProblemSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    input_description = serializers.CharField(required=True)
    output_description = serializers.CharField(required=True)
    samples = serializers.ListField(required=True, child=AddSampleSerializer(), allow_empty=False)
    hint = serializers.CharField(required=True)
    problem_source = serializers.CharField(required=True)
    time_limit = serializers.IntegerField(required=True)
    memory_limit = serializers.IntegerField(required=True)
    tags = serializers.ListField(required=True, child=serializers.CharField(max_length=150), allow_empty=True)
    visible = serializers.BooleanField(required=True)
    in_battle_set = serializers.BooleanField(required=True)
    difficulty = serializers.CharField(required=True)


class AdminAddTagSerializer(serializers.Serializer):
    tag = serializers.CharField(required=True)


class AdminGetProblemListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    input_description = serializers.CharField()
    output_description = serializers.CharField()
    samples = serializers.ListField(child=AddSampleSerializer())
    hint = serializers.CharField()
    problem_source = serializers.CharField()
    time_limit = serializers.IntegerField()
    memory_limit = serializers.IntegerField()
    tags = serializers.ListField(child=serializers.CharField(max_length=150))
    visible = serializers.BooleanField()
    in_battle_set = serializers.BooleanField()
    difficulty = serializers.CharField()
    created_by = serializers.CharField()


class AdminGetProblemByIDSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)


class ReturnAdminGetProbelmByIDSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField()
    input_description = serializers.CharField()
    output_description = serializers.CharField()
    samples = serializers.ListField(child=AddSampleSerializer())
    hint = serializers.CharField()
    problem_source = serializers.CharField()
    time_limit = serializers.IntegerField()
    memory_limit = serializers.IntegerField()
    tags = serializers.ListField(child=serializers.CharField(max_length=150))
    visible = serializers.BooleanField()
    in_battle_set = serializers.BooleanField()
    difficulty = serializers.CharField()
    created_by = serializers.CharField()


class UserGetProblemInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Problem
        fields = ('id', 'title', 'description', 'input_description', 'output_description', 'samples',
                    'hint', 'problem_source', 'time_limit', 'memory_limit', 'tags', 'difficulty', 'submission_number',
                    'ac_number')


class UserGetProblemInfoByIDSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)


class UserGetProblemListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    time_limit = serializers.IntegerField()
    memory_limit = serializers.IntegerField()
    submission_number = serializers.IntegerField()
    ac_number = serializers.IntegerField()


class UploadFileSerializer(forms.Form):
    id = forms.IntegerField(required=True)
    file = forms.FileField(required=True)


class UserGetProblemSolutionListSerializer(serializers.Serializer):
    pro_id = serializers.IntegerField(required=True)


class UserGetProblemSolutionInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    author = serializers.CharField()
    content = serializers.CharField()
    last_update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")


class UserAddProblemSolutionSerializer(serializers.Serializer):
    pro_id = serializers.IntegerField()
    content = serializers.CharField()


class UserUpdateProblemSolutionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    content = serializers.CharField()