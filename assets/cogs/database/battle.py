import random
import asyncio
from aiosqlite import connect
import json

def get_path():
    with open('assets/config/paths.json', encoding='utf-8') as fh:
        json_txt = fh.read()
        json_txt = str(json_txt).replace("'", '"').replace('True', 'true').replace('False', 'false')
        paths_list = json.loads(json_txt)
        return paths_list


paths_list = get_path()

IMG_PATH = paths_list["ABS_PATH"] + paths_list["IMG_PATH"]
DB_PATH = paths_list["ABS_PATH"] + paths_list["DB_PATH"]
BG_PATH = paths_list["IMG_PATH"] + paths_list["BG_PATH"]
NONE_PATH = paths_list["IMG_PATH"] + paths_list["NONE_PATH"]
BG_TMP_PATH = paths_list["IMG_PATH"] + paths_list["BG_TMP_PATH"]
TREASURE_BOX_PATH = paths_list["IMG_PATH"] + "akuma.png"
SHOP_PATH = paths_list["IMG_PATH"] + "shop.png"

class Battle:

    def __init__(self, ctx=None, interaction=None):
        self.ctx = ctx
        self.interaction = interaction
        self.user = self.ctx.author if self.ctx else self.interaction.user
        self.user_id = self.user.id

    
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
    
