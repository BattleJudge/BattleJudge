from rest_framework import serializers


class UserSubmitCodeSerializer(serializers.Serializer):
    pro_id = serializers.IntegerField()
    code = serializers.CharField()
    language = serializers.CharField()


class UserGetSubmissionResultSerializer(serializers.Serializer):
    submission_id = serializers.IntegerField()


class ReturnUserGetSubmissionResultSerializer(serializers.Serializer):
    result = serializers.IntegerField()
    static_info = serializers.DictField()


class UserGetSubmissionList(serializers.Serializer):
    pro_id = serializers.IntegerField()
    page = serializers.IntegerField(required=False)
    size = serializers.IntegerField(required=False)


class ReturnUserGetSubmissionList(serializers.Serializer):
    id = serializers.IntegerField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    code = serializers.CharField()
    result = serializers.IntegerField()
    static_info = serializers.DictField()
    language = serializers.CharField()