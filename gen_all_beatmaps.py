import os
from imd_helper import convert_imd_to_mc_slide
import json

if not os.path.exists("tmp"):
    os.mkdir("tmp")

song_list = {
    "beiduofenbingdu": "贝多芬病毒",
    "yefengfeiwu": "野蜂飞舞",
    "canonrock": "卡农摇滚版",
    "keluodiya": "克罗地亚狂想曲",
    "shaonvqixiangqu": "少女绮想曲",
    "heianwangzi": "黑暗王子",
    "zisejiqing": "紫色激情",
    "toywar": "Toy War",
    "drama": "Drama",
    "taoyuanxiangwaixingren": "桃源乡的外星人",
    "qingniao": "青鸟",
    "nightoffire": "Night of Fire",
    "omaiga": "哦买嘎",
    "secondchoice": "Second Choice",
    "junwanghechu": "君往何处",
    "jixianshengcun": "极限生存挑战",
    "arklightrmver": "神圣之光",
    "hangengxman": "X-Man",
    "takemyhand": "Take My Hand",
    "shangxindrbtmg": "伤心的人别听慢歌",
    "dearmozart": "Dear Mozart",
    "takeflight": "Take Flight",
    "goldtown": "黄金之城",
    "reanimate": "暗夜苏醒",
    "shaonvhuanzang": "少女幻葬",
    "dajiahao": "大家好",
    "please": "Please",
    "megaburn": "心跳倒计时",
    "ineffabilis": "Ineffabilis",
    "doubleagent":"双重间谍",
    "rolypoly": "Roly Poly"
}


for song in song_list.keys():
    ch_name = song_list[song]
    print(song, ch_name)
    if not os.path.exists(f"tmp/{song}.jpg"):
        os.system(f"cp 节奏大师官方谱/{song}.jpg tmp/")

    if not os.path.exists(f"tmp/{song}.mp3"):
        os.system(f"cp 节奏大师官方谱/{song}.mp3 tmp/")

    data = convert_imd_to_mc_slide(song, ch_name)

    with open(f"tmp/{song}.mc", "w") as f:
        json.dump(data, f)

