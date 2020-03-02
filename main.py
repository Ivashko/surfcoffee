import telebot
import const
from telebot import types
import requests
from PIL import Image
from pyzbar.pyzbar import decode
bot = telebot.TeleBot(const.token)



A = ['55.822134,37.384924', '55.771663,37.682658', '55.761076,37.632374', '55.757391,37.622978',
             '55.754033,37.637354', '55.752040,37.670716', '55.745017,37.684479', '55.752604,37.597523',
             '55.742325,37.609997', '55.721476,37.611827', '55.693549,37.557648',
     '55.688152,37.615642', '55.663194,37.481396']
dic = {}
ad = ''
for i in range (len(A)-1):
    ad+=A[i]+'|'
ad+=A[len(A)-1]

def distance_calc(latlon,mode):
    global ad
    a = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=' + latlon + '&destinations=' + ad + '&mode=' + mode + '&language=ru&key=AIzaSyCcswgpnbZPAP4j1m91NRc2fnBfPO__APM'
    b = {}
    r = requests.get(a, params=b)
    data = r.json()
    err = (data['rows'][0]['elements'][0]['status'])
    if err != 'ZERO_RESULTS':
        distance = data['rows'][0]['elements'][0]['distance']['value']
        ind = 0
        for i in range (1,len(A)):
            if (data['rows'][0]['elements'][i]['distance']['value']) < distance:
                distance = data['rows'][0]['elements'][i]['distance']['value']
                ind = i
        if mode == 'walking':
            time = str(data['rows'][0]['elements'][ind]['duration']['text'])
        else:
            time = str(data['rows'][0]['elements'][ind]['duration_in_traffic']['text'])
        address = data['destination_addresses'][ind]
        return(distance, time, address, ind)
    else:
        return ('','','','')
# Стандартная клавиатура
@bot.message_handler(commands=['start'])
def handler_start(message):
    user_keyboard = telebot.types.ReplyKeyboardMarkup()
    user_keyboard.row('Моя карта', 'Новости')
    user_keyboard.row('Кофейни', 'Меню')
    bot.send_message(message.from_user.id, "Алоха, бро😎", reply_markup=user_keyboard)
# Клавиатура для кнопки (Моя карта)
@bot.message_handler(content_types=['text'])
def press_mycard(message):
    try:
        if message.text == 'Меню':
                user_keyboard_back = telebot.types.ReplyKeyboardMarkup()
                user_keyboard_back.row('Моя карта', 'Новости')
                user_keyboard_back.row('Кофейни', 'Меню')
                bot.send_message(message.from_user.id, '%s' %const.menu, reply_markup=user_keyboard_back)
        elif message.text == "Новости":
            bot.send_message(message.from_user.id, "Три последнии новости!")
            URL_VK = 'https://api.vk.com/method/wall.get?domain=surfcoffee&count=10&v=5.74&filter=owner&access_token=012c6a2d9bad7caebbe3e95a23a23e8f0dca7abe2b3d1bcc2b893d590f223af1a1e928d87583a96713200'
            w = {}
            l = requests.get(URL_VK, params=w)
            data2 = l.json()
            try:
                if data2['response']['items'][1]['text'] == '':
                    bot.send_message(message.from_user.id, '1) https://vk.com/surfcoffee?w=wall-464371_' + str(data2['response']['items'][1]['id']))
                else:
                    bot.send_message(message.from_user.id, '1)' + data2['response']['items'][1]['text'])
            except Exception:
                print()
            for i in range(10):
                try:
                    s1 = 'C:/Users/Ivan/PycharmProjects/location/photo/news1.' + str(i) +'.jpg'
                    bot.send_photo(message.from_user.id, open(s1, 'rb'))
                except Exception:
                    print()
            try:
                if data2['response']['items'][2]['text'] == '':
                    bot.send_message(message.from_user.id, '2) https://vk.com/surfcoffee?w=wall-464371_' + str(data2['response']['items'][2]['id']))
                else:
                    bot.send_message(message.from_user.id, '2)' + data2['response']['items'][2]['text'])
            except Exception:
                print()
            for i in range(10):
                try:
                    s2 = 'C:/Users/Ivan/PycharmProjects/location/photo/news2.' + str(i) +'.jpg'
                    bot.send_photo(message.from_user.id, open(s2, 'rb'))
                except Exception:
                    print()
            try:
                if data2['response']['items'][3]['text'] == '':
                    bot.send_message(message.from_user.id, '3) https://vk.com/surfcoffee?w=wall-464371_' + str(data2['response']['items'][3]['id']))
                else:
                    bot.send_message(message.from_user.id, '3)' + data2['response']['items'][3]['text'])
            except Exception:
                print()
            for i in range (10):
                try:
                    s3 = 'C:/Users/Ivan/PycharmProjects/location/photo/news3.' + str(i) +'.jpg'
                    bot.send_photo(message.from_user.id, open(s3, 'rb'))
                except Exception:
                    print()
    # Моя карта
        elif message.text == 'Моя карта':
            mycard_keyboard = telebot.types.ReplyKeyboardMarkup(True)
            mycard_keyboard.row('Узнать баланс', 'Назад')
            bot.send_message(message.from_user.id, "Выберите", reply_markup=mycard_keyboard)
        elif message.text == 'Узнать баланс':
            bot.send_message(message.from_user.id, "Отправь фотку QR кода с обратной стороны карты")
    # Назад
        elif message.text == 'Назад':
            try:
                del dic[message.from_user.id]
                del dic[str(message.from_user.id)]
            except Exception:
                print()
            user_keyboard_back = telebot.types.ReplyKeyboardMarkup()
            user_keyboard_back.row('Моя карта', 'Новости')
            user_keyboard_back.row('Кофейни', 'Меню')
            bot.send_message(message.from_user.id, "Выберите", reply_markup=user_keyboard_back)
    # Кофейни
        elif message.text == 'Кофейни':
            user_keyboard = telebot.types.ReplyKeyboardMarkup(True)
            user_keyboard.row('Ближайшая кофейня', 'Посмотреть все адреса', 'Назад')
            bot.send_message(message.from_user.id, "Выберите", reply_markup=user_keyboard)
        elif message.text == 'Ближайшая кофейня':
            keyboard = types.ReplyKeyboardMarkup(True)
            button_geo = types.KeyboardButton(text='Отправить геолокацию', request_location=True)
            keyboard.add(button_geo)
            bot.send_message(message.from_user.id, 'Отправь мне своё местоположение!', reply_markup=keyboard)
        elif message.text == 'Посмотреть все адреса':
            bot.send_message(message.from_user.id, 'Перейдите по ссылке: https://www.google.com/maps/d/u/0/edit?mid=1uy5NOjQzmv_o0YjL0s17279nTRe35_42&ll=55.773651838993%2C37.51691856768127&z=11')
        else:
            if message.text == 'На машине':
                hide_markup = types.ReplyKeyboardMarkup(True)
                hide_markup.row('Ближайшая кофейня', 'Посмотреть все адреса', 'Назад')
                bot.send_message(message.from_user.id, 'Поиск ближайшей кофейни с учётом пробок...', reply_markup = hide_markup)
                dic[str(message.from_user.id)] = 'driving&departure_time=now'
                if dic.get(message.from_user.id)==None:
                    keyboard = types.ReplyKeyboardMarkup(True)
                    button_geo = types.KeyboardButton(text='Отправить местоположение', request_location=True)
                    keyboard.add(button_geo)
                    bot.send_message(message.from_user.id, 'Произошла ошибка')
                    bot.send_message(message.from_user.id, 'Пожалуйста отправьте свои координаты', reply_markup=keyboard)

            elif message.text == 'Пешком':
                hide_markup = types.ReplyKeyboardMarkup(True)
                hide_markup.row('Ближайшая кофейня', 'Посмотреть все адреса', 'Назад')
                dic[str(message.from_user.id)] = 'walking'
                bot.send_message(message.from_user.id, 'Поиск ближайшей кофейни...', reply_markup = hide_markup)
                if dic.get(message.from_user.id)==None:
                    keyboard = types.ReplyKeyboardMarkup(True)
                    button_geo = types.KeyboardButton(text='Отправить местоположение', request_location=True)
                    keyboard.add(button_geo)
                    bot.send_message(message.from_user.id, 'Произошла ошибка')
                    bot.send_message(message.from_user.id, 'Пожалуйста отправьте свои координаты', reply_markup=keyboard)

            a=None
            if dic.get(message.from_user.id)!=None:
                a = dic[message.from_user.id]
                del dic[message.from_user.id]
            if a!=None:
                distance, time, address, ind = distance_calc(a, dic[str(message.from_user.id)])
                if distance != '':

                    st = A[ind].split(',')
                    bot.send_location(message.from_user.id, float(st[0]),float(st[1]))
                    bot.send_message(message.from_user.id,'Адрес ближайшего SurfCoffee: %s.' %address)
                    bot.send_message(message.from_user.id, 'Ваше расстояние до ближайшего SurfCoffee: %s м.' %distance)
                    bot.send_message(message.from_user.id, 'Время в пути до ближайшего SurfCoffee: %s' %time )
                    del dic[str(message.from_user.id)]
                else:
                    bot.send_message(message.from_user.id, 'Невозможно проложить маршрут!')
                    del dic[str(message.from_user.id)]
    except Exception:
        bot.send_message(message.from_user.id, 'Зря ты так много запросов отправлял ☠')
        bot.send_message(message.from_user.id, 'Теперь жди пока бот пофиксит ошибку с этим запросом, это займет около 5 минут 🤬')
# Кофейни
@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        hide_markup = types.ReplyKeyboardMarkup(True)
        hide_markup.row('На машине', 'Пешком', 'Назад')
        bot.send_message(message.from_user.id, 'Спасибо!', reply_markup=hide_markup)
        bot.send_message(message.from_user.id, 'Как ты будешь добираться до SurfCoffee?')
        dic[message.from_user.id] = str(message.location.latitude) + ',' + str(message.location.longitude)
# Фото
@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    fileName = str(str(message.chat.id) + '.jpg')
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = 'C:/Users/Ivan/PycharmProjects/location/' + fileName
    with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
    bot.reply_to(message, "QRcode обрабатывается")
    try:
        qr_code = decode(Image.open(fileName))
        cardNum = str(qr_code).split()[0][16:-2]
        bot.send_message(message.from_user.id, '%s' %cardNum)
    except Exception:
        bot.send_message(message.from_user.id, 'Произошла ошибка. Отправь фотографию еще раз!')

bot.polling(none_stop=True)
