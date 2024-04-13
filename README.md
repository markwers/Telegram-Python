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

def edit_login(chat_id, site_name, new_login):
    conn = psycopg2.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME,
        port=PORT
    )
    cur = conn.cursor()
    cur.execute("UPDATE users_data SET login = %s WHERE chat_id = %s AND site_name = %s", (new_login, chat_id, site_name))
    conn.commit()
    cur.close()
    conn.close()

@dp.message_handler(commands=["help"])
async def help_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    await message.answer('команды:', reply_markup=keyboard)
    await message.answer("/help - все команды")
    await message.answer("/start - начать сначала")
    await message.answer("/save - сохранить")
    await message.answer("/editlogin - изменить логин")
    await message.answer("/editpassword - изменить пароль")
    await message.answer("/show - вывести все сохранения")
    await message.answer("/delete - удалить то, что вы сохранили")

def edit_db(login, password, site_name):
    conn = psycopg2.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME,
        port=PORT
    )
    cur = conn.cursor()
    cur.execute("UPDATE users_data SET login = %s, password = %s WHERE site_name = %s", (login, password, site_name))
    conn.commit()
    cur.close()
    conn.close()

@dp.message_handler(commands=['editlogin'])
async def edit_login_command(message: types.Message):
    data = message.text.split()[1:]
    if len(data) == 2:
        site_name, new_login = data
        chat_id = message.chat.id
        edit_login(chat_id, site_name, new_login)
        await message.answer(f"Логин для сайта {site_name} успешно изменен на {new_login}")
    else:
        await message.answer("Неправильный формат. Пожалуйста введите /editlogin название_сайта новый_логин")

def edit_password(chat_id, site_name, new_password):
    conn = psycopg2.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME,
        port=PORT
    )
    cur = conn.cursor()
    cur.execute("UPDATE users_data SET password = %s WHERE chat_id = %s AND site_name = %s", (new_password, chat_id, site_name))
    conn.commit()
    cur.close()
    conn.close()

def get_saved_info(chat_id):
    conn = psycopg2.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME,
        port=PORT
    )
    cur = conn.cursor()
    cur.execute("SELECT site_name, login, password FROM users_data WHERE chat_id = %s", (chat_id,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

@dp.message_handler(commands=['show'])
async def show_handler(message: types.Message):
    chat_id = message.chat.id
    saved_info = get_saved_info(chat_id)
    if saved_info:
        response = "Сохраненные данные:\n"
        for site_name, login, password in saved_info:
            response += f"Сайт: {site_name}\nЛогин: {login}\nПароль: {password}\n\n"
        await message.answer(response)
    else:
        await message.answer("Нет сохраненной информации.")

@dp.message_handler(commands=['editpassword'])
async def edit_password_command(message: types.Message):
    data = message.text.split()[1:]
    if len(data) == 2:
        site_name, new_password = data
        chat_id = message.chat.id
        edit_password(chat_id, site_name, new_password)
        await message.answer(f"Пароль для сайта {site_name} успешно изменен на {new_password}")
    else:
        await message.answer("Неправильный формат. Пожалуйста введите /editpassword название_сайта новый_пароль")

if __name__ == '__main__':
    executor.start_polling(dp)
