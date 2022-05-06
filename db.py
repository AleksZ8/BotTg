import sqlite3 as sql
from button.buttons_menu import profile_button


def sql_connect():
    global db, cur
    db = sql.connect('telegram.db')
    cur = db.cursor()
    if db:
        print('соединение')
    db.execute("""
    CREATE TABLE IF NOT EXISTS
    menu(
        id INT AUTO_INCREMENT,
        photo TEXT,
        name TEXT NOT NULL,
        text TEXT,
        PRIMARY KEY (id)
    )
    """)
    db.commit()


async def db_import(data):
    async with data.proxy() as d:
        cur.execute('INSERT INTO menu(photo, name, text) VALUES (?, ?, ?)', tuple(d.values()))
        db.commit()
        print('ЗАКОМИЧЕНО')


async def db_load(message):
    for i in cur.execute('SELECT photo, name, text from menu').fetchall():
        await message.answer_photo(i[0],  f'{i[1]},\n {i[2]}', reply_markup=profile_button)
        print('DONE')
    # await message.answer('Команды для общения с ботом.', reply_markup=user_buttons)

#
# async def db_delete(meesage):
#     for i in cur.execute('SELECT id, photo, name, text from menu').fetchall():
#         await meesage.answer_photo(i[1],  f'{i[2]},\n {i[3]}', reply_markup=delete)
