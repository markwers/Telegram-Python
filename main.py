import psycopg2
from aiogram import Bot, Dispatcher, types, executor
Token = '6906826308:AAErg5mP2jMkbhuPKT2ulWCR4hPUmLUCY68'
HOST = "192.168.1.24"
PASSWORD = "postgres"
PORT = "5424"
USER = "postgres"
DB_NAME = "чернушеч"
bot = Bot(token=Token)
dp = Dispatcher(bot)

def save_to_db(chat_id, login, password, site_name):
    conn = psycopg2.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME,
        port=PORT
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO users_data (chat_id, login, password, site_name) VALUES (%s, %s, %s, %s)", (chat_id, login, password, site_name))
    conn.commit()
    cur.close()
    conn.close()

def passwordbysite(chat_id, site_name=None):
    conn = psycopg2.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME,
        port=PORT
    )
    cur = conn.cursor()
    if site_name:
        cur.execute("SELECT * FROM users_data WHERE chat_id = %s AND site_name = %s", (chat_id, site_name))
    else:
        cur.execute("SELECT * FROM users_data WHERE chat_id = %s", (chat_id,))
    stolbs = cur.fetchall()
    cur.close()
    conn.close()
    saved_passwords = "Сохраненные пароли:\n"
    for stolb in stolbs:
        saved_passwords += f"ID: {stolb[0]}, Логин: {stolb[2]}, Пароль: {stolb[3]}, Сайт: {stolb[4]}\n"
    return saved_passwords

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    await message.answer(f"ведите /help {user_full_name}")
@dp.message_handler(commands=["help"])
async def help_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer('команды:', reply_markup=keyboard)
    await message.answer("/help - все команды")
    await message.answer("/start - начать с начала")
    await message.answer("/save- сохронить")
    await message.answer("/editlogin - изменить логин")
    await message.answer("/editpassword - изменить пароль")
    await message.answer("/show - вывести все сахронения")
    await message.answer("/delete - удолить то что вы сохронили")


def save_to_db(login, password, site_name):

    conn = psycopg2.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME,
        port=PORT
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO passwords3 (login, password, site_name) VALUES (%s, %s, %s)", (login, password, site_name))
    conn.commit()
    cur.close()
    conn.close()
def edit_db(login, password, site_name):
    conn = psycopg2.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME,
        port=PORT
    )
    cur = conn.cursor()
    if login:
        cur.execute("UPDATE passwords3 SET login = %s WHERE site_name = %s", (login, site_name))
    elif password:
        cur.execute("UPDATE passwords3 SET password = %s WHERE site_name = %s", (password, site_name))
    conn.commit()
    cur.close()
    conn.close()
@dp.message_handler(commands=['editlogin'])
async def edit_login_command(message: types.Message):
    data = message.text.split()[1:]
    if len(data) == 2:
        site_name, new_login = data
        edit_db(new_login, None, site_name)
        await message.answer(f"Логин для сайта {site_name} успешно изменен")
    else:
        await message.answer("Неправильный формат. Пожалуйста введите /editlogin название сайта новый логин")

@dp.message_handler(commands=['editpassword'])
async def edit_password_command(message: types.Message):
    data = message.text.split()[1:]
    if len(data) == 2:
        site_name, new_password = data
        edit_db(None, new_password, site_name)
        await message.answer(f"Пароль для сайта {site_name} успешно изменен")
    else:
        await message.answer("Неправильный формат. Пожалуйста введите /editpassword название сайта новый пароль")
def password_by_site(site_name=None):
    conn = psycopg2.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME,
        port=PORT
    )
    cur = conn.cursor()
    if site_name:
        cur.execute("SELECT * FROM passwords3 WHERE site_name = %s", (site_name,))
    else:
        cur.execute("SELECT * FROM passwords3")
        rows = cur.fetchall()
    cur.close()
    conn.close()
    saved_passwords = "Сохраненные пароли:\n"
    for row in rows:
        saved_passwords += f"ID: {row[0]}, Логин: {row[1]}, Пароль: {row[2]}, Сайт: {row[3]}\n"
    return saved_passwords

@dp.message_handler(commands=['show'])
async def show_all_passwords(message: types.Message):
    data = message.text.split()[1:]
    if data:
        site_name = " ".join(data)
        passwords = password_by_site(site_name)
    else:
        passwords = password_by_site()
    await message.answer(passwords)

@dp.message_handler(commands=['save'])
async def save_to_db_command(message: types.Message):
    data = message.text.split()[1:]
    if len(data) == 3:
        login, password, site_name = data
        save_to_db(login, password, site_name)
        await message.answer("Логин, пароль и название сайта успешно сохранено")
    else:
        await message.answer("Неправильный формат. Пожалуйста введите /save логин пароль название сайта")

def delete_from_db(site_name):
    conn = psycopg2.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME,
        port=PORT
    )
    cur = conn.cursor()
    cur.execute("DELETE FROM passwords3 WHERE site_name = %s",
                (site_name,))
    conn.commit()
    cur.close()
    conn.close()
@dp.message_handler(commands=['delete'])
async def delete_from_db_command(message: types.Message):
    data = message.text.split()[1:]
    if data:
        site_name = " ".join(data)
        delete_from_db(site_name)
        await message.answer(f"Данные для сайта {site_name} успешно удалены")
    else:
        await message.answer("Неправильный формат. Пожалуйста введите /delete название сайта")

def on_startup(dispatcher):
    print("Бот готов к работе!")
    init_db()
def init_db():
    conn = psycopg2.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME,
        port=PORT
    )
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS passwords3 (id SERIAL PRIMARY KEY, login TEXT NOT NULL, password TEXT NOT NULL, site_name TEXT NOT NULL)")
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    init_db()
    executor.start_polling(dp)
