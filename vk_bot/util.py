import vk_api, math, random, requests, base64, wikipedia, subprocess
from vk_api.utils import get_random_id
from loadevn import group_idd, apinews
from vk_bot.core.sql.vksql import *
from vk_bot.core.sql.sqlgame import hellosql
from vk_api import VkUpload
from datetime import timedelta
import pyPrivnote
wikipedia.set_lang("ru")
helpspisok = ["/help", "/хелп", "/начать", "/помощь", "/команды", "/старт"]
help = """Дроу. Ето бот команды овощей. Возможности:
🧾Калькулятор - передавать значения через пробел: /калькулятор 2 + 2
☁/погода - мона писать город на русском, не сработает = ингиш, игнор = ошибка
❤привет\споки - :З
🐱 /каты - скинет пикчу котика или неко
🇬🇧 - /переводчик
🏳‍🌈/яой, юри, трапы, геббельс, махно, калян, мем, ноги\ножки, адольф\гитлер, хес - сделает вашу жизнь лучше 🌚
а так же, ключ -c может указать количество пикч.
Например: /яой -c 7
👍🏻/оцени - оценка по 10ти бальной шкале
📚 /вики - информация из вики
🎬/видео название - рандомное видео с вашим названием
✔/вероятность /шансы - вероятность чего либо
🌚/хентай - 🌚🌚🌚
❓/выбери - /выбери огурцы с молоком или гречка с кетчупом
🐴/смех - генератор смеха, с -h выдаст справку
👅/повтори - повторение вашего сообщения
💾/гиф или /док - скинет вам гифку или документ с переданным названием
&#128064;/кто - выбирает рандомного человека в беседе под вашим предлогом
&#128181;/курс - курс доллара и евро
⚰/дата - когда произойдет переданное вами событие
🎲/число - выбрать число из диапазона. Пример: /число 1 500
&#128101;/онлайн - покажет онлайн беседы
👤/префикс - как вас будет называть бот
💱/конвертер - конвертер валюты, с usd и eur (/конвертер 5000 usd)
🔒/зашифровать <ваш текст> /расшифровать <Текст, который вернул бот после шифрования>
📰/новость - покажет последние новости
&#128102;/профиль - информация о вашем профиле
📝/бинарный0/1: 0 - зашифрует текст в бинарный код, а 1 - расшифрует
🏝/перешли - пересылает фото для сохранения
🔍/аниме на фото - подскажет вам аниме изображенное на фото
👋🏻/приветствие - устанавливает приветствие для новых участников беседы
📚/альбомы - настройка вашего личного альбома. Вызов без всего скинет справку
📋/айди - скинуть цифровой айди группы\человека, например: /айди slava_air
🔒/encodeqr - зашифрует текст в qrcode , /decodeqr - расшифрует qrcode
📁/группы - настройка ваших групп, из которых будет браться рандомный пост
✍🏻/длина - сколько символов в вашем сообщение, не считая саму команду
🔒/пароль - Сгенерирует пароль. Можно передавать длину /пароль 69, ежели не передать - буит 64
💰/чекни донат - проверить, донатили ли вы и сколько
📺/посты - поисков постов, по переданным тегам или тексту
github.com/anar66/vk-bot
"""
def translit(text, vk=False, english=False):
    apikey = "trnsl.1.1.20190508T201810Z.385ebfa1e596baa0.90672cf8655555b1b51ced31b03c2e8bb9bde46c"
    url = "https://translate.yandex.net/api/v1.5/tr.json/translate"
    url2 = "https://translate.yandex.net/api/v1.5/tr.json/detect"
    params = {"key": apikey,
                "text":text[1:]}
    r = requests.get(url2, params=params)
    encode = r.json()
    lang = f"{encode['lang']}-ru"
    if english:
        lang = "ru-en"
    params = {"key": apikey,
            "text":text[0:],
            "lang":lang}
    r = requests.get(url, params=params)
    encode = r.json()
    try:
        if vk:
            encode = " ".join(encode["text"][1:])
            return {"message":"Перевод: {}".format(encode),}
    except:
        return
    return encode["text"][0]
def shellrun(text):
    text = " ".join(text[1:])
    try:
        result = subprocess.check_output(text, shell=True, encoding="utf-8")
    except:
        return {"message":"!error"}
    return {"message":result}

def weather(text):
    try:
        qr = text[1]
    except:
        return
    q = translit(text=qr, english=True); q.lower()
    apiurl = "http://api.openweathermap.org/data/2.5/find"
    appid = '22c7bf8e593c47b0cf88f390e8e5376a'
    params = {
                'q': q,
                'appid': appid,
                'units': 'metric',
                'lang': 'ru'
                }
    try:
        r = requests.get(apiurl, params=params, timeout=5)
        encode = r.json()
        w = encode['list'][0]['weather'][0]['description']
        temp = encode["list"][0]["main"]["temp"]
        vlaga = encode["list"][0]["main"]["humidity"]
        wind = encode["list"][0]["wind"]["speed"]
    except:
        return
    return {"message":f"""Город: {q}
    🌥Погода: {w}
    🌡Температура: {temp}°
    💧Влажность: {vlaga}
    💨Скорость ветра: {wind}м/с""",
    }
def answer(text):
    zapros = text[0].lower()
    if zapros == "споки" or zapros == "спокойной":
        answer = ["Спотьки", "Спокойной ночи", "Спи, но я приду и выебу тебя историей аир"
                  ,"Сладких снов", "Эротишных снов🌚🌚🌚"]
    else:
        answer = ["Кук", "зиг хайль", "куку нахуй",
                   "🇺🇦слава украине🇺🇦", "здравствуй", "здравия желаю"]
    return {"message":random.choice(answer),}
def status(vk, msgcount):
    vk.status.set(text=f"✉сообщений: {msgcount}", group_id=group_idd)
def callall(vk, event):
    calllist = []
    callid = vk.messages.getConversationMembers(peer_id=event.object.peer_id)
    for a in callid:
        calllist.append(f"@id{str(a['id'])} ({a['first_name']} {a['last_name']})")
    calljoin = ", ".join(calllist)
    return {"message":f"Я ПРИЗЫВАЮ ВАС:\n{calljoin}"}
def getusername(vk, uid):
    try:
        requests = vk.users.get(user_ids=uid, fields="first_name")
    except vk_api.exceptions.ApiError:
        return
    response = requests[0]["first_name"]
    return response
def vkbase64(text, encode=False, decode=False):
    text = " ".join(text[1:])
    try:
        if encode:
            result = base64.b64encode(bytes(text, 'utf-8'))
        else:
            result = base64.b64decode(text)
    except:
        return {"message":"!error"}
    return {"message":result.decode('utf-8')}
def profile(uid, mc2):
    msg = checktable('messages', 'id', uid)["msg"]
    xp = checktable('level', 'id', uid)["xp"]
    levelxp = 500
    level = 0
    while xp > levelxp:
        levelxp = levelxp * 2.5
        level += 1
    if mc2["admins"]:
        user = "Админ😎"
    elif mc2["vips"]:
        user = "Вип🤵"
    else:
        user = "Юзер"
    G = checktable("economy","id", uid)["money"]
    return {"message": f"""Твой профиль:
👦| Роль: {user}
🔑| Префикс: {mc2['prefix']}
📃| Айди: id{uid}
✉ | Сообщения: {msg}
💰| G: {G}$
🎮| XP: {xp}
⭐| Уровень: {level}"""}
def nametoid(vk, text):
    try:
        text = text[1]
        result = vk.utils.resolveScreenName(screen_name=text)
        if result["type"] == "group":
            result = "-" + str(result["object_id"])
        else:
            result = result["object_id"]
    except KeyboardInterrupt:
        return {"message":"!error"}
    return {"message":f"Айди: {result}"}
def tasks():
    ltasks = """🚫мать панель
    ✅рассылка
    ✅ооп
    ✅многопоток
    ✅работа с пикчами
    🚫экономика\рпг
    ✅кеш
    ✅несколько личных альбомов для випов
    ✅отношения с детоводством
    ✅автоконвентор айди в тех же альбомах
    ✅список идей
    ✅приветствие
    ✅личные альбомы
    ✅аниме на фото"""
    return {"message":ltasks}
def gethistorytols(vk, event):
    history = vk.messages.getHistory(count=0, user_id=event.user_id)["count"]
    return {"message":f"сообщений в лс: {history}"}
def nuke():
    return {"message":"ВСЕ ПИЗДА ИВАНУ. /запустил ядерную боеголовку в максбота/", "attachment":"video162900694_456239801"}
