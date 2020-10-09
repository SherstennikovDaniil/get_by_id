from TikTokApi import TikTokApi
import sqlite3


api = TikTokApi()
db = sqlite3.connect('data.db')
cr = db.cursor()

list = []
with open("id_list.txt", "r", encoding='utf-8') as txt:
    for line in txt:
        if "Username" in line:
            a = line.split(':')
            b = [str(a[1]).strip()]
            list = list + b


def get_by_nick(id):
    try:
        data = api.getUser(id)
        uid = data["userInfo"]["user"]["uniqueId"]
        nick = data["userInfo"]["user"]["nickname"]
        subs = data["userInfo"]["stats"]["followerCount"]
        likes = data["userInfo"]["stats"]["heartCount"]
        link = "https://www.tiktok.com/@" + id
        cr.execute(f"SELECT id FROM table1 WHERE id = '{uid}'")
        if cr.fetchone() is None:
            cr.execute(f"INSERT INTO table1 VALUES (?, ?, ?, ?, ?)", (uid, nick, subs, likes, link))
            db.commit()
            print("Сделали ", id)
        else:
            print(id, 'уже есть.')
    except:
        print(id, '-хуесос.')


if __name__ == "__main__":
    try:
        for id in list:
            get_by_nick(id)
            list.pop([id])
    except:
        print("скрипт слетел, но не ссым")
