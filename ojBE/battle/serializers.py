from rest_framework import serializers
from account.models import UserProfile
from .models import Battle


class BattleRecordSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    player1_id = serializers.IntegerField()
    player2_id = serializers.IntegerField()
    result = serializers.CharField()
    pro_id = serializers.IntegerField()
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")


class BattleRankSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('nickname', 'battle_score', 'battle_win', 'battle_lose')


class GetBattleSubmissionRecordSerializer(serializers.Serializer):
    battle_id = serializers.IntegerField()


class ReturnBattleSubmissionRecordSerializer(serializers.Serializer):
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    code = serializers.CharField()
    result = serializers.IntegerField()
    static_info = serializers.DictField()
    language = serializers.CharField()