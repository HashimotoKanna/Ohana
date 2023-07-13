class Battle:
    def __init__(self, ctx=None, interaction=None, config=None):
        self.ctx = ctx
        self.interaction = interaction
        self.user = self.ctx.author if self.ctx else self.interaction.user
        self.user_id = self.user.id
        self.config = config

    async def battle(self):
        enemy_hp = 100
        player_hp = 150

        enemy_dmg = 30
        player_dmg = 50

        player_exp = 0
        give_exp = 100
        text = f"敵のhp:{enemy_hp}\nプレイヤーのhp:{player_hp}"
        while True:
            player_hp -= enemy_dmg
            text = f"敵の攻撃！ プレイヤーは{enemy_dmg}ダメージを受けた！"

            if player_hp < 0:
                text = "プレイヤーの負け"
                break
            enemy_hp -= player_dmg
            text = f"プレイヤーの攻撃！敵に{player_dmg}ダメージを与えた！"

            if enemy_hp < 0:
                player_exp += give_exp
                text = f"敵に勝利しました！\n{give_exp}を獲得しました！"
                break

        text = f"敵のhp:{enemy_hp}\nプレイヤーのhp:{player_hp}"

    async def experience():
        return
