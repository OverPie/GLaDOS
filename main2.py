#!/usr/bin/python3.7
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from token2 import *
from util import *
from photo import *
from smeh import *
# from wall import post
import vk_api, requests, sys
from threading import Thread
vk_session = vk_api.VkApi(token=token)
vk_session2 = vk_api.VkApi(token=token22)
vk = vk_session.get_api()
vk2 = vk_session2.get_api()
longpoll = VkBotLongPoll(vk_session, group_idd)
msgcount = 0
# timestatus = nowtime()
# varlalle = Thread(target=post, args=(vk, vk2), daemon=True)
# varlalle.start()
try:
    for event in longpoll.listen():
        try:
            vk.groups.enableOnline(group_id=group_idd)
        except vk_api.exceptions.ApiError:
            None
        response = {"message":None}
        if event.object.text:
            text = event.object.text.split()
            try:
                requests = text[0].lower()
            except IndexError:
                continue
            if requests == "/калькулятор":
                response = calc(text)
            elif requests == "/погода":
                response = weather(text)
            elif requests == "слава":
                response = {"message":"🇺🇦украине🇺🇦"}
            elif requests in ["привет", "ку", "зиг", "споки", "спокойной"]:
                response = answer(text)
            elif requests == "/off" and event.user_id == 367919273:
                sys.exit()
            elif requests in helpspisok:
                response = {"message":help}
            elif requests == "/красилов":
                vk.messages.send(user_id=event.user_id, random_id=get_random_id(),
                                message="Krasyliv")
            elif requests == "/каты":
                response = cats(vk2, text)
            elif requests == "/переводчик":
                response = translit(text, vk)
            elif requests == "/юри":
                response = yuri(vk2, text)
            elif requests == "/геббельс":
                response = gebbels(vk2, text)
            elif requests == "/яой":
                response = yaoi(vk2, text)
            elif requests == "/трапы":
                response = trap(vk2, text)
            elif requests == "/лоли":
                response = loli(vk2,text)
            elif requests == "/оцени":
                response = doulikethis(text)
            elif requests == "/вики":
                response = wiki(text)
            elif requests == "/махно":
                response = mahno(vk2, text)
            elif requests == "/цитаты":
                response = citati(vk2, text)
            elif requests == "/калян":
                response = colyan(vk2, text)
            elif requests == "/видео":
                response = video(vk2, text)
            elif requests == "/вероятность" or requests == "/шансы":
                response = chance(text)
            elif requests == "/хентай":
                response = hentai(vk2, text)
            elif requests == "/выбери":
                response = oror(text)
            elif requests == "/смех":
                response = smex(text)
            elif requests == "/повтори":
                response = repeat(text)
            elif requests == "/док" or requests == "/гиф":
                response = rdocs(vk2, text)
            elif requests == "/ноги" or requests == "/ножки":
                response = legs(vk2, text)
            elif requests == "/мем":
                response = mem(vk2, text)
            elif requests == "/кто":
                response = who(vk, event, text)
            elif requests == "/курс":
                response = valute(text)
            elif requests == "/дата":
                response = date(text)
            elif requests == "/число":
                response = number(text)
            elif requests == "/онлайн" or requests == "/online":
                response = online(vk, event)
            elif requests == "/адольф" or requests == "/гитлер":
                response = adolf(vk2, text)
        try:
            if response["message"]:
                if "attachment" not in response:
                    response["attachment"] = None
                if event.chat_id:
                    vk.messages.send(chat_id=event.chat_id, random_id=get_random_id(),
                                    message=response["message"], attachment=response["attachment"])
                else:
                    vk.messages.send(user_id=event.object.from_id, random_id=get_random_id(),
                                    message=response["message"], attachment=response["attachment"])
                msgcount += 1
                status(vk2, msgcount)
        except TypeError:
            continue
except KeyboardInterrupt:
    sys.exit()
