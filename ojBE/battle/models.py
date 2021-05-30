from django.db import models

class BattleResult(object):
    PLAYER1_WIN = "player1"
    PLAYER2_WIN = "player2"
    DRAWN_GAME = "drawn game"

class Battle(models.Model):
    player1_id = models.IntegerField()
    player1_code = models.TextField()
    player1_endtime = models.DateTimeField()
    
    player2_id = models.IntegerField()
    player2_code = models.TextField()
    player2_endtime = models.DateTimeField()

    result = models.TextField()
    pro_id = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "battle"

class BattleUser(models.Model):
    user_id = models.IntegerField()
    pro_id = models.IntegerField(default=None)
    channels_name = models.TextField()
    opponent_channels_name = models.TextField(default=None)
    waiting = models.BooleanField(default=True)
    battle_id = models.IntegerField(default=None)

    class Meta:
        db_table = "battle_user"
