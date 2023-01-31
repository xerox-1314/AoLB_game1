import sqlite3 as sq

conn = sq.connect('game_db.db')
cur = conn.cursor()


def get_all_levels():
    return cur.execute(f"""SELECT num, name FROM levels""").fetchall()


def get_characters():
    print(cur.execute(f"""SELECT * FROM characters""").fetchall())
    return cur.execute(f"""SELECT * FROM characters""").fetchall()


def get_count_now():
    return cur.execute(f"""SELECT count FROM game_info""").fetchone()[0]


def get_character_now():
    id = cur.execute("""SELECT character_now FROM game_info""").fetchone()[0]
    character_now = cur.execute(f"""SELECT * FROM characters WHERE id = '{id}'""").fetchone()
    return character_now


def change_character(id):
    cur.execute(f"""UPDATE game_info SET character_now = '{id}'""")
    conn.commit()


def buy_character(id):
    character = cur.execute(f"""SELECT * FROM characters WHERE id = '{id}'""").fetchone()
    count_now = cur.execute(f"""SELECT count FROM game_info""").fetchone()[0]
    print(character)
    print(count_now)
    if character[3] <= count_now:
        cur.execute(f"""UPDATE characters SET buyed = '1' WHERE id = '{id}'""")
        cur.execute(f"""UPDATE game_info SET count = '{count_now - character[3]}'""")
        conn.commit()
        return True
    else:
        return False


def add_money():
    cur.execute(f"""UPDATE game_info SET count = '{get_count_now() + 1}'""")
    conn.commit()


