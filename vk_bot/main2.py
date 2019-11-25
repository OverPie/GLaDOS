#!/usr/bin/python3.7
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api import VkUpload
from loadevn import *
from vk_bot.core.sql.vksql import *
from vk_bot.core.utils.botutil import *
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
import pylibmc
import vk_api
import logging
import datetime
from vk_bot.core.sql.sqlgame import *
import mods
import sys
import argparse


class Main:
    """
    Инит главного класса, токен - токен группы
    токен22 - токен страницы, который нужен шоб кидать пикчи из пабликов
    при иницилизации класса, т.е t = Main(123, 123) - запускается усе добро
    типа авторизиации, настройки потоков и импорта модулей
    дальше можно запустить метод run(t.run()), щобы заставить бота работать
    """

    def __init__(self, token, token22):
        self.token = token
        self.token22 = token22
        self.argsdebug()
        self.authorization()
        self.thread()
        self.modules = mods.modules

    def authorization(self):
        vk_session = vk_api.VkApi(token=token, api_version=5.102)
        vk_session2 = vk_api.VkApi(token=token22)
        self.vk = vk_session.get_api()
        self.vk2 = vk_session2.get_api()
        self.upload = VkUpload(vk_session)
        self.longpoll = VkBotLongPoll(vk_session, group_idd)
        self.message = 0

    def thread(self):
        self.pool = ThreadPoolExecutor(8)
        self.futures = []

    def argsdebug(self):
        args = argparse.ArgumentParser(description="параметры запуска бота")
        args.add_argument('-d', '--debug',  action='store_true',
                          default=False, dest="debug")
        try:
            args = args.parse_args(sys.argv[1:])
        except:
            self.debug = False
            return
        self.debug = args.debug

    def checkthread(self):
        """
        Скинуть название исключения в потоке, ежели  такое произойдет
        """
        for x in as_completed(self.futures):
            if x.exception() != None:
                logging.error(x.exception())
                print(f"ошибОЧКА разраба: {x.exception()}")
            self.futures.remove(x)
            logging.info("Поток закрылся")

    def run(self):
        logging.info("Запуск бота")
        self.mc = pylibmc.Client(["127.0.0.1"])
        for event in self.longpoll.listen():
            if self.debug:
                self.lobby(event)
            else:
                self.futures.append(self.pool.submit(self.lobby, event))
                self.pool.submit(self.checkthread)

    def lobby(self, event):
        action = event.object.action
        if action:
            action = action['type']
        else:
            action = False
        try:
            attachmentype = event.object.attachments[0]['type']
        except:
            attachmentype = False
        # какой ивент прислал вк. Например message_new
        events = event.type.value
        logging.info(f"Событие: {events}")
        # остатки прошлой цивилизации, скоро выкинем
        try:
            text = event.object.text.split()
        except:
            text = []
        uid = event.object.from_id
        if uid == None:
            uid = event.object['user_id']
        logging.info(
            f"Сообщение: {event.object.text}  От: {uid}  В: {event.object.peer_id}")
        """
        mc и mc2 = Кеш, щобы каждый раз не делать запросы в бд
        mc = сервер с мемкешем
        а mc2 = то чо он вернул на юзера, который тригернул бота
        подробнее о том, чо хранится в кеше -
        мона глянуть в core/utils/botutil.py
        """
        mc2 = sqlcache(self.mc, uid)
        prefix = mc2["prefix"]
        if mc2["ban"]:
            return
        try:
            requests = text[0].lower()
            uberequests = " ".join(text[0:]).lower()
        except IndexError:
            requests = [None]
            uberequests = [None]
        """
        Эта страшная хероборина снизу отвечает за проверку и запуск модулей
        щобы ее получше понять, читаните core/modules/ или коммент снизу
        module.included = Включен ли модуль. По дефолту True
        module.vktypes = Список ивентов вк, при которых надо запустить модуль. По деофлту - ["message_new"]
        module.available_for = кому доступен модуль. По дефолту users, так же есть vips и admins
        module.attachment  = нужно ли модуль чота прикрепить, и ежели да - то чо
        Типы (module.types):
        Типы определяют то, как запустится модуль и чо ему для этого нужно
        Дефолтный тип - command
        C него и начнем:
        В данном типы вы должны прописать в модуле переменную command, размером в одно слово
        и ежели юзер напишет его(а так же все прошлые проверки, о которых я сказал выше - пройдут)
        запустится ваш модуль.
        runalways - запуск модуля без команды, просто основываясь на проверках выше
        specialcommand так же, как и в обычнос command - нужно прописать команду
        но, юзеру можно буит писать чота прямо в ней, например: /команда666
        Пример использования - личные альбомы или группы
        """
        for module in self.modules:
            run = False
            if module.included and events in module.vktypes and mc2[module.available_for] and action == module.action:
                if module.types == "command":
                    if requests in module.command or uberequests in module.uberequests:
                        run = True
                elif module.types == "runalways":
                    run = True
                elif module.types == "commandb":
                    command = module.getcommand(uid, requests)
                    if requests == command:
                        run = True
                elif module.types == "specialcommand":
                    rlen = len(module.command[0])
                    if requests[:rlen] == module.command[0]:
                        run = True
                if module.attachment:
                    if attachmentype != module.attachment:
                        run = False
                if run:
                    module = module(self.vk, self.vk2, self.upload)
                    module.givedata(uid=uid, text=text, event=event, mc2=mc2,
                                    prefix=prefix, peer=event.object.peer_id, mc=self.mc)
                    module.makeothervariables()
                    then = datetime.datetime.now()
                    if module.thread == False:
                        logging.info(f"Запуск модуля {module.__module__}")
                        module.main()
                        now = datetime.datetime.now()
                        delta = now - then
                        logging.info(
                            f"{module.__module__} завершил свою работу через {delta.total_seconds()} секунд")
                    else:
                        self.pool.submit(module.main)


# прост логирование
logging.basicConfig(level=logging.INFO, filename="bot.log",
                    format='%(asctime)s - %(message)s')
t = Main(token, token22)
t.run()
