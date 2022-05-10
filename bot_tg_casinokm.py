import telebot
import random
import sqlite3
from telebot import types

config = {
    'token': '5181040190:AAEX7p18RHUQWcqk3GvO5kOfyn7Lsaw5h9w'
}


play = None
points_play = 0
play_game_coloda = []
play_game = []
stavka = None
russian_roulette = 'russian roulette'
blackjack = 'blackjack'
cb = None
balance = None
card = None
coloda = [['♠', 'Туз', 11], ['♥', 'Туз', 11], ['♦', 'Туз', 11], ['♣', 'Туз', 11], ['♠', 'Король', 5], ['♥', 'Король', 5], ['♦', 'Король', 5], ['♣', 'Король', 5],
          ['♠', 'Дама', 4], ['♥', 'Дама', 4], ['♦', 'Дама', 4], ['♣', 'Дама', 4], ['♠', 'Валет', 3], ['♥', 'Валет', 3], ['♦', 'Валет', 3], ['♣', 'Валет', 3],
          ['♠', '10', 10], ['♥', '10', 10], ['♦', '10', 10], ['♣', '10', 10], ['♠', '9', 9], ['♥', '9', 9], ['♦', '9', 9], ['♣', '9', 9],
          ['♠', '8', 8], ['♥', '8', 8], ['♦', '8', 8], ['♣', '8', 8], ['♠', '7', 7], ['♥', '7', 7], ['♦', '7', 7], ['♣', '7', 7],
          ['♠', '6', 6], ['♥', '6', 6], ['♦', '6', 6], ['♣', '6', 6]]
proverka_par = [['Туз', 'Туз']]
play_coloda = None
client = telebot.TeleBot(config['token'])


@client.message_handler(commands=['start'])
def start(message):
    client.send_message(message.chat.id, f'{message.from_user.first_name}, приветствую в нашем казино.')

    client.send_message(message.chat.id, 'Для просмотра всех команд, пропишите /info.')


@client.message_handler(commands=['info'])
def get_info(message):
    client.send_message(message.chat.id,
        '/reg - Регистрация пользователя\n/cash - Просмотр баланса\n/casino - Играть в казино\n/delete - Удаление своего аккаунта')


@client.message_handler(commands=['reg'])
def reg(message):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        id INT,
        nickname VARCHAR(255),
        cash INT
    )""")
    db.commit()
    cursor.execute(f"SELECT id FROM users WHERE id = {message.chat.id}")
    if cursor.fetchone() is None:
        client.send_message(message.chat.id,
                            'Для регистрации напишите имя, которое будет использоваться для игр.\nПример указан ниже')
        primer = client.send_message(message.chat.id, 'Кирилл Косыгин')
        client.register_next_step_handler(primer, nickreg)
    else:
        client.send_message(message.chat.id, 'Вы уже были зарегистрированы.\nВаши данные указаны ниже')
        for i in cursor.execute(f"SELECT nickname FROM users WHERE id = {message.chat.id}"):
            q = 'nickname: ' + i[0]
            client.send_message(message.chat.id, q)
        for i in cursor.execute(f"SELECT cash FROM users WHERE id = {message.chat.id}"):
            q = 'cash: ' + str(i[0])
            client.send_message(message.chat.id, q)


@client.message_handler(commands=['cash'])
def printcash(message):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()
    for i in cursor.execute(f"SELECT cash FROM users WHERE id = {message.chat.id}"):
        q = 'cash: ' + str(i[0])
        client.send_message(message.chat.id, q)


@client.message_handler(commands=['delete'])
def deluser(message):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()
    cursor.execute("SELECT id FROM users WHERE id = {}".format(message.chat.id))
    if cursor.fetchone() is None:
        client.send_message(message.chat.id, 'Пользователь не найден')
    else:
        cursor.execute('DELETE FROM users WHERE id = {}'.format(message.chat.id))
        db.commit()
        client.send_message(message.chat.id, 'Ваш аккаунт успешно удален')


@client.message_handler(commands=['casino'])
def casino(message):
    global russian_roulette
    global blackjack
    db = sqlite3.connect('server.db')
    cursor = db.cursor()
    cursor.execute(f"SELECT id FROM users WHERE id = {message.chat.id}")
    if cursor.fetchone() is None:
        client.send_message(message.chat.id, 'Для продолжения игры, зарегистрируйтесь /reg.')
    else:
        db = sqlite3.connect('server.db')
        cursor = db.cursor()
        for i in cursor.execute(f"SELECT cash FROM users WHERE id = {message.chat.id}"):
            proverka = i[0]
        if proverka != 0:
            markup_inline = types.InlineKeyboardMarkup()
            item_blackjack = types.InlineKeyboardButton(text='Blackjack', callback_data=blackjack)
            item_roulette = types.InlineKeyboardButton(text='Russian roulette', callback_data=russian_roulette)
            item_wikiblackjack = types.InlineKeyboardButton(text='Что за игра↑',
                                                            url='https://ru.wikipedia.org/wiki/Блэкджек')
            item_wikiroulette = types.InlineKeyboardButton(text='Что за игра↑',
                                                           url='https://ru.wikipedia.org/wiki/Русская_рулетка')
            markup_inline.row(item_blackjack, item_roulette)
            markup_inline.row(item_wikiblackjack, item_wikiroulette)
            client.send_message(message.chat.id, 'Выберите одну игру из множества',
                                reply_markup=markup_inline
                                )
        else:
            for i in cursor.execute(f"SELECT cash FROM users WHERE id = {message.chat.id}"):
                client.send_message(message.chat.id, f'Ваш баланс составляет: {i[0]}')
            client.send_message(message.chat.id, 'Пополните баланс')


@client.message_handler(content_types=['text'])
def stavka(message):
    client.send_message(message.chat.id, 'Неизвестная команда')
    """
    db = sqlite3.connect('server.db')
    cursor = db.cursor()
    global stavka
    if message.text == 'Va-банк':
        stavka = cursor.execute(f"SELECT cash FROM users WHERE id = {message.chat.id}")
    else:
        try:
            stavka = int(message.text)
        except:
            markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_50 = types.KeyboardButton(50)
            item_100 = types.KeyboardButton(100)
            item_200 = types.KeyboardButton(200)
            item_500 = types.KeyboardButton(500)
            item_1000 = types.KeyboardButton(1000)
            item_2000 = types.KeyboardButton(2000)
            item_5000 = types.KeyboardButton(5000)
            item_10000 = types.KeyboardButton(10000)
            item_vabank = types.KeyboardButton('Va-банк')
            markup_reply.add(item_50, item_100, item_200, item_500, item_1000,
                item_2000, item_5000, item_10000, item_vabank
            )
            primer = client.send_message(message.chat.id, 'Такой ставки не существует\nВыберите ставку или напишите свою',
                reply_markup=markup_reply
            )
            client.register_next_step_handler(primer, stavka1)
"""



@client.callback_query_handler(func=lambda call: True)
def casino_play(callback):
    global play
    global points_play
    global play_game_coloda
    client.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id,
        text='Выберите одну игру из множества'
    )
    if callback.data == 'blackjack':
        play = 'blackjack'
        points_play = 0
        play_game_coloda = []
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_50 = types.KeyboardButton(50)
        item_100 = types.KeyboardButton(100)
        item_200 = types.KeyboardButton(200)
        item_500 = types.KeyboardButton(500)
        item_1000 = types.KeyboardButton(1000)
        item_2000 = types.KeyboardButton(2000)
        item_5000 = types.KeyboardButton(5000)
        item_10000 = types.KeyboardButton(10000)
        item_vabank = types.KeyboardButton('Va-банк')
        markup_reply.add(item_50, item_100, item_200, item_500, item_1000,
                         item_2000, item_5000, item_10000, item_vabank)
        primer = client.send_message(callback.message.chat.id, 'Выберите вашу ставку или напишите свою',
            reply_markup=markup_reply
        )
        client.register_next_step_handler(primer, stavka1)
    elif callback.data == 'russian roulette':
        play = 'russian roulette'
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_50 = types.KeyboardButton(50)
        item_100 = types.KeyboardButton(100)
        item_200 = types.KeyboardButton(200)
        item_500 = types.KeyboardButton(500)
        item_1000 = types.KeyboardButton(1000)
        item_2000 = types.KeyboardButton(2000)
        item_5000 = types.KeyboardButton(5000)
        item_10000 = types.KeyboardButton(10000)
        item_vabank = types.KeyboardButton('Va-банк')
        markup_reply.add(item_50, item_100, item_200, item_500, item_1000,
                         item_2000, item_5000, item_10000, item_vabank)
        primer = client.send_message(callback.message.chat.id, 'Выберите вашу ставку или напишите свою',
            reply_markup=markup_reply
        )
        client.register_next_step_handler(primer, stavka1)


def nickreg(message):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()
    a = message.text
    cursor.execute("INSERT INTO users VALUES ({}, '{}', {})".format(message.chat.id, str(a), 10000))
    db.commit()
    client.send_message(message.chat.id, 'Регистрация прошла успешно')
    client.send_message(message.chat.id, 'Ваши данные вы можете прочитать в сообщениях ниже.')
    for i in cursor.execute(f"SELECT nickname FROM users WHERE id = {message.chat.id}"):
        q = 'nickname: ' + i[0]
        client.send_message(message.chat.id, q)
    for i in cursor.execute(f"SELECT cash FROM users WHERE id = {message.chat.id}"):
        q = 'cash: ' + str(i[0])
        client.send_message(message.chat.id, q)


def play_roulette(message):
    global stavka
    db = sqlite3.connect('server.db')
    cursor = db.cursor()
    if message.text == 'Да':
        for i in cursor.execute(f'SELECT cash FROM users WHERE id = {message.chat.id}'):
            balance = i[0]
        num = random.randrange(1, 7)
        if num == 1:
            client.send_message(message.chat.id, 'Вы выиграли')
            cursor.execute(f'UPDATE users SET cash = {stavka * 5 + balance} WHERE id = {message.chat.id}')
            db.commit()
        else:
            client.send_message(message.chat.id, 'Вы проиграли')
            cursor.execute(f'UPDATE users SET cash = {balance - stavka} WHERE id = {message.chat.id}')
            db.commit()
            client.send_message(message.chat.id, 'Для просмотра баланса, напишите /cash.')
    else:
        client.send_message(message.chat.id, 'Для просмотра всех команд, напишите /info.')
        return True


def play_blackjack1(message):
    global stavka
    global play_coloda
    global play_game
    global card
    global play_game_coloda
    global points_play
    if message.text == 'Нет':
        points()
        if points_play < 20:
            db = sqlite3.connect('server.db')
            cursor = db.cursor()
            for i in cursor.execute(f'SELECT cash FROM users WHERE id = {message.chat.id}'):
                balance = i[0]
            cursor.execute(f'UPDATE users SET cash = {abs(stavka - balance)} WHERE id = {message.chat.id}')
            db.commit()
            markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_info = types.KeyboardButton('/info')
            markup_reply.add(item_info)
            client.send_message(message.chat.id, 'Ваша колода:')
            for i in range(len(play_game_coloda)):
                card = ''.join(play_game_coloda[i][:-1])
                client.send_message(message.chat.id, card)
            client.send_message(message.chat.id, 'Вы проиграли',
                reply_markup=markup_reply
            )
        elif points_play >= 20:
            db = sqlite3.connect('server.db')
            cursor = db.cursor()
            for i in cursor.execute(f'SELECT cash FROM users WHERE id = {message.chat.id}'):
                balance = i[0]
            cursor.execute(f'UPDATE users SET cash = {stavka + balance} WHERE id = {message.chat.id}')
            db.commit()
            markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_info = types.KeyboardButton('/info')
            markup_reply.add(item_info)
            client.send_message(message.chat.id, 'Ваша колода:')
            for i in range(len(play_game_coloda)):
                card = ''.join(play_game_coloda[i][:-1])
                client.send_message(message.chat.id, card)
            client.send_message(message.chat.id, 'Вы выиграли',
                reply_markup=markup_reply
            )
        return True
    elif message.text == 'Да' and play_game == 'Открытый':
        card = random.choice(play_coloda)
        play_coloda.remove(card)
        play_game_coloda.append(card)
        client.send_message(message.chat.id, 'Ваша колода:')
        for i in range(len(play_game_coloda)):
            card = ''.join(play_game_coloda[i][:-1])
            client.send_message(message.chat.id, card)
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_yes = types.KeyboardButton('Да')
        item_no = types.KeyboardButton('Нет')
        markup_reply.add(item_yes, item_no)
        points()
        if points_play == 21:
            db = sqlite3.connect('server.db')
            cursor = db.cursor()
            for i in cursor.execute(f'SELECT cash FROM users WHERE id = {message.chat.id}'):
                balance = i[0]
            cursor.execute(f'UPDATE users SET cash = {stavka + balance} WHERE id = {message.chat.id}')
            db.commit()
            play_game_coloda = []
            points_play = 0
            play_coloda = []
            markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_info = types.KeyboardButton('/info')
            markup_reply.add(item_info)
            client.send_message(message.chat.id, 'Вы выиграли',
                reply_markup=markup_reply
            )
            return True
        elif points_play > 21:
            db = sqlite3.connect('server.db')
            cursor = db.cursor()
            for i in cursor.execute(f'SELECT cash FROM users WHERE id = {message.chat.id}'):
                balance = i[0]
            cursor.execute(f'UPDATE users SET cash = {abs(stavka - balance)} WHERE id = {message.chat.id}')
            db.commit()
            play_game_coloda = []
            points_play = 0
            play_coloda = []
            client.send_message(message.chat.id, 'Перебор')
            markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_info = types.KeyboardButton('/info')
            markup_reply.add(item_info)
            client.send_message(message.chat.id, 'Для просмотра всех команд, пропишите /info.',
                reply_markup=markup_reply
            )
            return True
        else:
            q = 'Ваши очки:' + str(points())
            client.send_message(message.chat.id, q)
            primer = client.send_message(message.chat.id, 'Взять еще одну карту?',
                reply_markup=markup_reply
            )
            client.register_next_step_handler(primer, play_blackjack1)
    elif message.text == 'Да' and play_game == 'Закрытый':
        card = random.choice(play_coloda)
        play_coloda.remove(card)
        play_game_coloda.append(card)
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_yes = types.KeyboardButton('Да')
        item_no = types.KeyboardButton('Нет')
        markup_reply.add(item_yes, item_no)
        points()
        if points_play > 21:
            db = sqlite3.connect('server.db')
            cursor = db.cursor()
            for i in cursor.execute(f'SELECT cash FROM users WHERE id = {message.chat.id}'):
                balance = i[0]
            cursor.execute(f'UPDATE users SET cash = {abs(stavka - balance)} WHERE id = {message.chat.id}')
            db.commit()
            play_game_coloda = []
            points_play = 0
            play_coloda = []
            client.send_message(message.chat.id, 'Перебор')
            markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_info = types.KeyboardButton('/info')
            markup_reply.add(item_info)
            client.send_message(message.chat.id, 'Для просмотра всех команд, пропишите /info.',
                reply_markup=markup_reply
            )
            return True
        else:
            primer = client.send_message(message.chat.id, 'Взять еще одну карту?',
                reply_markup=markup_reply
            )
            client.register_next_step_handler(primer, play_blackjack1)
    elif message.text == 'Закрытый':
        play_game = message.text
        for _ in range(2):
            card = random.choice(play_coloda)
            play_coloda.remove(card)
            play_game_coloda.append(card)
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_yes = types.KeyboardButton('Да')
        item_no = types.KeyboardButton('Нет')
        markup_reply.add(item_yes, item_no)
        points()
        if points_play > 21:
            db = sqlite3.connect('server.db')
            cursor = db.cursor()
            for i in cursor.execute(f'SELECT cash FROM users WHERE id = {message.chat.id}'):
                balance = i[0]
            cursor.execute(f'UPDATE users SET cash = {abs(stavka - balance)} WHERE id = {message.chat.id}')
            db.commit()
            play_game_coloda = []
            points_play = 0
            play_coloda = []
            client.send_message(message.chat.id, 'Перебор')
            client.send_message(message.chat.id, 'Для просмотра всех команд, пропишите /info.')
            return True
        else:
            primer = client.send_message(message.chat.id, 'Взять еще одну карту?',
                reply_markup=markup_reply
            )
            client.register_next_step_handler(primer, play_blackjack1)
    elif message.text == 'Открытый':
        play_game = message.text
        for _ in range(2):
            card = random.choice(play_coloda)
            play_coloda.remove(card)
            play_game_coloda.append(card)
        client.send_message(message.chat.id, 'Ваша колода:')
        for i in range(2):
            card = ''.join(play_game_coloda[i][:-1])
            client.send_message(message.chat.id, card)
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_yes = types.KeyboardButton('Да')
        item_no = types.KeyboardButton('Нет')
        markup_reply.add(item_yes, item_no)
        points()
        if points_play == 21:
            play_game_coloda = []
            points_play = 0
            play_coloda = []
            client.send_message(message.chat.id, 'Вы выиграли')
            client.send_message(message.chat.id, 'Для просмотра всех команд, пропишите /info.')
            return True
        elif points_play > 21:
            play_game_coloda = []
            points_play = 0
            play_coloda = []
            client.send_message(message.chat.id, 'Перебор')
            client.send_message(message.chat.id, 'Для просмотра всех команд, пропишите /info.')
            return True
        else:
            q = 'Ваши очки:' + str(points())
            client.send_message(message.chat.id, q)
            primer = client.send_message(message.chat.id, 'Взять еще одну карту?',
                reply_markup=markup_reply
            )
            client.register_next_step_handler(primer, play_blackjack1)
    else:
        client.send_message(message.chat.id, 'Для просмотра всех команд, пропишите /info.')


def stavka1(message):
    global stavka
    global play
    db = sqlite3.connect('server.db')
    cursor = db.cursor()
    try:
        if message.text == 'Va-банк':
            stavka = cursor.execute(f"SELECT cash FROM users WHERE id = {message.chat.id}")
        else:
            stavka = int(message.text)
        if play == 'russian roulette':
            markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_yes = types.KeyboardButton('Да')
            item_no = types.KeyboardButton('Нет')
            markup_reply.add(item_yes, item_no)
            primer = client.send_message(message.chat.id, 'Шанс выигрыша равен 16.67%, продолжить?',
                reply_markup=markup_reply
            )
            client.register_next_step_handler(primer, play_roulette)
        elif play == 'blackjack':
            markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_yes = types.KeyboardButton('Да')
            item_no = types.KeyboardButton('Нет')
            markup_reply.add(item_yes, item_no)
            primer = client.send_message(message.chat.id, 'Готовы играть?',
                reply_markup=markup_reply
            )
            client.register_next_step_handler(primer, play_blackjack)

    except:
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_50 = types.KeyboardButton(50)
        item_100 = types.KeyboardButton(100)
        item_200 = types.KeyboardButton(200)
        item_500 = types.KeyboardButton(500)
        item_1000 = types.KeyboardButton(1000)
        item_2000 = types.KeyboardButton(2000)
        item_5000 = types.KeyboardButton(5000)
        item_10000 = types.KeyboardButton(10000)
        item_vabank = types.KeyboardButton('Va-банк')
        markup_reply.add(item_50, item_100, item_200, item_500, item_1000,
            item_2000, item_5000, item_10000, item_vabank
        )
        primer = client.send_message(message.chat.id, 'Такой ставки не существует\nВыберите ставку или напишите свою',
            reply_markup=markup_reply
        )
        client.register_next_step_handler(primer, stavka1)


def play_blackjack(message):
    if message.text == 'Да':
        global coloda
        global play_coloda
        global points_play
        points_play = 0
        random.shuffle(coloda)
        play_coloda = coloda[::]
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_close = types.KeyboardButton('Закрытый')
        item_open = types.KeyboardButton('Открытый')
        markup_reply.add(item_close, item_open)
        primer = client.send_message(message.chat.id, 'Выберите тип игры.',
            reply_markup=markup_reply
        )
        client.register_next_step_handler(primer, play_blackjack1)
    else:
        client.send_message(message.chat.id, 'Для просмотра всех команд, пропишите /info.')


def points():
    global play_game_coloda
    global points_play
    points_play = 0
    for i in range(len(play_game_coloda)):
        if play_game_coloda[i][1] == '6':
            points_play += 6
        elif play_game_coloda[i][1] == '7':
            points_play += 7
        elif play_game_coloda[i][1] == '8':
            points_play += 8
        elif play_game_coloda[i][1] == '9':
            points_play += 9
        elif play_game_coloda[i][1] == '10':
            points_play += 10
        elif play_game_coloda[i][1] == 'Туз':
            points_play += 11
        elif play_game_coloda[i][1] == 'Король':
            points_play += 4
        elif play_game_coloda[i][1] == 'Дама':
            points_play += 3
        elif play_game_coloda[i][1] == 'Валет':
            points_play += 2
    if points_play == 21:
        play_game_coloda = []
        return 'Вы выиграли'
    elif points_play > 21:
        play_game_coloda = []
        return 'Перебор'
    return points_play


client.polling(none_stop=True, interval=0)