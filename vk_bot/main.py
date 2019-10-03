from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from token2 import *
from util import *
from photo import *
from smeh import *
import vk_api, requests, sys
from vksql import *
from yourphoto import *
def mainlobby():
    vk_session = vk_api.VkApi(token=token22)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    try:
        for event in longpoll.listen():
            response = {"message":None}
            if "text" in dir(event) and "user_id" in dir(event):
                if event.from_me:
                    uid = recipient
                else:
                    uid = event.user_id
                if uid in allowuser and "chat_id" not in dir(event):
                    text = event.text.split()
                    try:
                        requests = text[0].lower()
                        uberequests = " ".join(text[0:]).lower()
                    except IndexError:
                        continue
                    if event.from_me:
                        uid = recipient
                    else:
                        uid = event.user_id
                    uname = getusername(vk,uid)
                    if requests == "/калькулятор":
                        response = calc(text)
                    elif requests == "/погода":
                        response = weather(text)
                    elif requests == "/шелл" and uid == 367919273:
                        response = shellrun(text)
                    elif requests == "слава":
                        response = {"message":"🇺🇦украине🇺🇦", "attachment":None}
                    elif requests in ["привет", "ку", "зиг", "споки", "спокойной"]:
                        response = answer(text)
                    elif requests == "/off" and event.user_id == 367919273:
                        sys.exit()
                    elif requests == "/help" or requests == "/хелп":
                        response = {"message":help, "attachment":None}
                    elif requests == "/красилов":
                        vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                                        message="Krasyliv")
                    elif requests == "/каты":
                        response = cats(vk,text)
                    elif requests == "/переводчик":
                        response = translit(text, vk)
                    elif requests == "/юри":
                        response = yuri(vk, text)
                    elif requests == "/геббельс":
                        response = gebbels(vk, text)
                    elif requests == "/яой":
                        response = yaoi(vk, text)
                    elif requests == "/трапы":
                        response = trap(vk, text)
                    elif requests == "/лоли":
                        response = loli(vk, text)
                    elif requests == "/оцени":
                        response = doulikethis(text)
                    elif requests == "/вики":
                        response = wiki(text)
                    elif requests == "/махно":
                        response = mahno(vk, text)
                    elif requests == "/цитаты":
                        response = citati(vk, text)
                    elif requests == "/калян":
                        response = colyan(vk, text)
                    elif requests == "/видео":
                        response = video(vk, text)
                    elif requests == "/вероятность" or requests == "/шансы":
                        response = chance(text)
                    elif requests == "/выбери":
                        response = oror(text)
                    elif requests == "/смех":
                        response = smex(text, uid)
                    elif requests == "/смехк":
                        response = smex(text, uid, db=True)
                    elif requests == "/повтори":
                        response = repeat(text)
                    elif requests == "/док" or requests == "/гиф":
                        response = rdocs(vk, text)
                    elif requests == "/ноги" or requests == "/ножки":
                        response = legs(vk,text)
                    elif requests == "/мем":
                        response = mem(vk, text)
                    elif requests == "/кто":
                        response = who(vk, event, text)
                    elif requests == "/курс":
                        response = valute(text)
                    elif requests == "/дата":
                        response = date(text)
                    elif requests == "/число":
                        response = number(text)
                    elif requests == "/адольф" or requests == "/гитлер":
                        response = adolf(vk, text)
                    elif requests == "/префикс":
                        response = update(uid, uname, text)
                    elif requests == "/жив?":
                        response = ping()
                    elif requests == "/конвертер":
                        response = convvalute(text)
                    elif requests == "/зашифровать":
                        response = vkbase64(text, encode=True)
                    elif requests == "/расшифровать":
                        response = vkbase64(text, decode=True)
                    elif requests == "/айди":
                        response = nametoid(vk,  text)
                    elif requests == "/идеи":
                        response = tasks()
                    elif requests == "/бинарный0":
                        response = text_to_bits(text)
                    elif requests == "/бинарный1":
                        response = text_from_bits(text)
                    elif requests == "/длина":
                        response = lentomsg(text)
                    elif requests == getcommand(uid, requests):
                        response = sendyourphoto(vk, text, uid, requests)
                    elif "".join(text)[:8] == "/альбомы":
                        response = photoadd(vk, uid, text, number=text)

                try:
                    if response["message"]:
                        if "attachment" not in response:
                            response["attachment"] = None
                        prefix = saveload(uid, uname)
                        # if "chat_id" in dir(event):
                        #     vk.messages.send(chat_id=event.chat_id, random_id=get_random_id(),
                        #                     message="от бота: " + response["message"], attachment=response["attachment"])
                        vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                                         message=f"от бота: {prefix['name']}, {response['message']}",
                                         attachment=response["attachment"])
                except TypeError:
                    continue
    except KeyboardInterrupt:
        sys.exit()
mainlobby()
