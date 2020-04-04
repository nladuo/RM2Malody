import os


def download_files(song):
    mp3_url = f"http://game.ds.qq.com/Com_SongRes/song/{song}/{song}.mp3"
    jpg_url = f"http://game.ds.qq.com/Com_SongRes/song/{song}/{song}.jpg"
    imd_url = f"http://game.ds.qq.com/Com_SongRes/song/{song}/{song}_4k_hd.imd"

    os.system(f"wget {mp3_url}")
    os.system(f"wget {jpg_url}")
    os.system(f"wget {imd_url}")


song_list = [
    # "beiduofenbingdu",
    # "yefengfeiwu",
    # "canonrock", #卡农
    # "keluodiya",
    # "shaonvqixiangqu",
    # "heianwangzi",
    # "zisejiqing",
    # "toywar",
    # "drama",
    # "taoyuanxiangwaixingren", # 桃源乡的外星人
    # "qingniao",
    # "nightoffire",
    # "omaiga",
    # "secondchoice",
    "junwanghechu",
    # "jixianshengcun",
    # "arklightrmver",  # 神圣之光
    # "hangengxman",  # X-Man
    # "takemyhand",
    # "shangxindrbtmg",  # 伤心的人别听慢歌
    # "dearmozart",
    # "takeflight",
    # "goldtown",
    # "reanimate", # 暗夜苏醒
    # "shaonvhuanzang", # 少女幻葬
    # "dajiahao",
    # "please",
    # "megaburn",
    # "ineffabilis",
    # "doubleagent",
    # "rolypoly"
]


for s in song_list:
    download_files(s)
