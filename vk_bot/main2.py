#!/usr/bin/python3.7
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from token2 import *
from util import *
from photo import *
from smeh import *
import vk_api, requests, sys
from vksql import saveload
session = requests.Session()
vk_session = vk_api.VkApi(token=token)
vk_session2 = vk_api.VkApi(token=token22)
vk = vk_session.get_api()
vk2 = vk_session2.get_api()
upload = VkUpload(vk)
longpoll = VkBotLongPoll(vk_session, group_idd)
msgcount = 0
from vksql import *
from botutil import *
from yourphoto import *
from yourgroup import *
from relation import *

try:
    for event in longpoll.listen():
        if event.type == VkBotEventType.GROUP_JOIN:
            groupjoin(vk, event)
        if event.type == VkBotEventType.WALL_POST_NEW:
            sendpost(vk, event)
        try:
            vk.groups.enableOnline(group_id=group_idd)
        except vk_api.exceptions.ApiError:
            None
        response = {"message":None}
        try:
            if event.object.action['type'] == 'chat_invite_user':
                vk.messages.send(chat_id=event.chat_id, random_id=get_random_id(), message=checktable(chathello, 'id', event.chat_id)['hello'])
        except TypeError:
            None
        except vk_api.exceptions.ApiError:
            vk.messages.send(chat_id=event.chat_id, random_id=get_random_id(), message="Приветствие настроено не правильно!")
        if event.object.text:
            if "chat_id" in dir(event):
                checkchat(event)
            text = event.object.text.split()
            uid = event.object.from_id
            uname = getusername(vk,uid)
            setmessages(uid)
            if checkban(uid) == "kill him":
                continue
            try:
                requests = text[0].lower()
                uberequests = " ".join(text[0:]).lower()
            except IndexError:
                continue
            if checktable("admins","id", uid):
                if requests == "/бан":
                    ban(event.object.reply_message['from_id'])
                elif requests == "/разбан":
                    unban(event.object.reply_message['from_id'])
                elif requests == "/рассылка":
                    sendall(event, text, vk)
                elif requests == "/шелл":
                    response = shellrun(text)
                elif requests == "/вип":
                    tableadd("vips", "id", event.object.reply_message['from_id'])
            if requests == "/калькулятор":
                response = calc(text)
            elif requests == "/погода":
                response = weather(text)
            elif requests == "слава":
                response = {"message":"🇺🇦украине🇺🇦"}
            elif requests in ["привет", "ку", "зиг", "споки", "спокойной"]:
                response = answer(text)
            elif requests == "/off" and event.from_id == 367919273:
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
                response = smex(text, uid)
            elif requests == "/смехк":
                response = smex(text, uid, db=True)
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
            # elif requests == "/призыв":
            #     response = callall(vk, event)
            elif requests == "/префикс":
                response = update(uid, uname, text)
            elif requests == "/жив?":
                response = ping()
            elif requests == "/конвертер":
                response = convvalute(text)
            elif requests == "/новость":
                response = news()
            elif requests == "/зашифровать":
                 response = vkbase64(text, encode=True)
            elif requests == "/расшифровать":
                 response = vkbase64(text, decode=True)
            elif requests == "/профиль":
                response = profile(event, uid, uname)
            elif requests == "/бинарный0":
                response = text_to_bits(text)
            elif requests == "/бинарный1":
                response = text_from_bits(text)
            elif requests == "/перешли":
                response = forward(event, vk, session, upload)
            elif requests == "/хес" or requests == "/хесус":
                response = hesus(vk2, text)
            elif uberequests == "/аниме на фото":
                response = anime(event)
            elif requests == "/айди":
                response = nametoid(vk2, text)
            elif requests == "/идеи":
                response = tasks()
            elif requests == "/приветствие":
                response = hello(chathello, event, vk, text)
            elif requests == "/encodeqr":
                response = qrcode(text, vk, upload, session)
            elif requests == "/decodeqr":
                response = encodeqr(event)
            elif requests == "/группы":
                response = groupadd(vk, uid, text)
            elif text[:2] == ['/отношения', 'встречаться']:
                response = relationmeet(text, vk, event)
            elif uberequests == "/отношения отклонить":
                response = reject(event)
            elif uberequests == "/отношения принять":
                response = accept(event)
            elif requests == "/длина":
                response = lentomsg(text)
            elif requests == getcommandpost(uid):
                response = sendyourpost(vk2, text, uid)
            elif requests == getcommand(uid, requests):
                response = sendyourphoto(vk2, text, uid, requests)
            if checktable("vips","id", uid):
                if "".join(text)[:8] == "/альбомы":
                    response = photoadd(vk2, uid, text, number=text)
            elif requests == "/альбомы":
                response = photoadd(vk2, uid, text)
        try:
            if response["message"]:
                prefix = saveload(uid, uname)
                if "attachment" not in response:
                    response["attachment"] = None

                if event.chat_id:
                    vk.messages.send(chat_id=event.chat_id, random_id=get_random_id(),
                                    message=f"{prefix['name']}, {response['message']}",
                                     attachment=response["attachment"])
                else:
                    vk.messages.send(user_id=event.object.from_id, random_id=get_random_id(),
                                    message=f"{prefix['name']}, {response['message']}",
                                    attachment=response["attachment"])
                msgcount += 1
                status(vk2, msgcount)
        except TypeError:
            continue
        except NameError:
            None
except KeyboardInterrupt:
    sys.exit()
