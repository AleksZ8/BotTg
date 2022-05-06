import sqlite3 as sql
from button.buttons_menu import profile_button


def sql_connect():
    global db, cur
    db = sql.connect('teg.db')
    cur = db.cursor()
    if db:
        print('соединение')
    cur.execute("CREATE TABLE IF NOT EXISTS menu(id INTEGER PRIMARY KEY AUTOINCREMENT,photo TEXT,name TEXT, text TEXT)")
    db.commit()


async def db_import(data):
    async with data.proxy() as d:
        cur.execute('INSERT INTO menu(photo, name, text) VALUES (?, ?, ?)', tuple(d.values()))
        db.commit()


async def db_load(message):
    for i in cur.execute('SELECT photo, name, text from menu').fetchall():
        await message.answer_photo(i[0],  f'{i[1]},\n {i[2]}', reply_markup=profile_button)


async def load_delete():
    return cur.execute('SELECT id, photo, name, text FROM menu').fetchall()


async def db_delete(num):
    cur.execute('DELETE FROM menu WHERE id == ?', (num,))
    print(f'запись под номером {num} удалена')
    db.commit()

