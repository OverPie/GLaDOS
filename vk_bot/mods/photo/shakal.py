from PIL import Image, ImageDraw
from vk_bot.config import *
import io
import requests
import random
import os
from vk_bot.core.modules.basicplug import BasicPlug
from vk_bot.core.modules.upload import Upload


class Shakal(BasicPlug, Upload):
    doc = "Шакалим"
    command = ("шакал",)

    def main(self):
        try:
            url = self.event.object['attachments'][0]['photo']['sizes'][-1]['url']
            img = requests.get(url).content
            f = io.BytesIO(img)
            image = Image.open(f)
            name = f"name{random.randint(0, 1000)}.jpg"
            quality = int(self.text[1])
            image.save(name, quality=quality)
            attachment = self.uploadphoto(name)
            self.sendmsg("Дэржите фотку", attachment)
        except IndexError:
            self.sendmsg("Для работы команды, нужно прикрепить пикчу и написать цифру от 1 до 100 (чем меньше цифра, тем хуже качество)")
        finally:
            os.remove(name)
