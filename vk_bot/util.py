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

def shellrun(text):
    text = " ".join(text[1:])
    try:
        result = subprocess.check_output(text, shell=True, encoding="utf-8")
    except:
        return {"message":"!error"}
    return {"message":result}

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
def gethistorytols(vk, event):
    history = vk.messages.getHistory(count=0, user_id=event.user_id)["count"]
    return {"message":f"сообщений в лс: {history}"}
