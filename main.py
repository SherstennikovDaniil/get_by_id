from TikTokApi import TikTokApi
import sqlite3
import sys

api = TikTokApi()
db = sqlite3.connect('data.db')
cr = db.cursor()
cr.execute("""CREATE TABLE IF NOT EXISTS users (
    uid TEXT,
    nick TEXT,
    subscribers BIGINT,
    likes BIGINT,
    link TEXT
)""")
db.commit()

list = []
with open("id_list.txt", "r", encoding='utf-8') as txt:
    for line in txt:
        if "Username" in line:
            a = line.split(':')
            b = [str(a[1]).strip()]
            list = list + b


def get_by_nick(id):
    try:
        cr.execute(f"SELECT uid FROM users WHERE uid = '{id}'") #на всякий случай подгружу ещё раз, этот код только что
        if cr.fetchone() is None:                               #роббил
            data = api.getUser(id)
            uid = data["userInfo"]["user"]["uniqueId"]
            nick = data["userInfo"]["user"]["nickname"]
            subs = data["userInfo"]["stats"]["followerCount"]
            likes = data["userInfo"]["stats"]["heartCount"]
            link = "https://www.tiktok.com/@" + id
            cr.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?)", (uid, nick, subs, likes, link))
            db.commit()
            print("Сделали ", id)
        else:
            print(id, 'уже есть.')
    except:
        print(id, '-хуесос.')


SCR_COUNT = 5
try:
    script_id = int(sys.argv[1])
except:
    script_id = 0

if __name__ == "__main__":
    while True:
        try:
            for (index, id) in enumerate(list):
                if index % SCR_COUNT == script_id:
                    get_by_nick(id)
        except:
            pass

