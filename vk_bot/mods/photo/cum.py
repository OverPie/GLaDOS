from vk_bot.core.modules.basicplug import BasicPlug
from vk_bot.core.modules.upload import Upload
import random
import os


class CamShot(BasicPlug, Upload):
    doc = "Сделать из фотки 'спасибо я кончил'"
    command = ["/спасибо"]

    def main(self):
        try:
            link = self.event.object['attachments'][0]['photo']['sizes'][-1]['url']
        except:
            self.sendmsg("пикчонку забыли")
            return
        randomnumber = random.randint(0, 10000)
        url = f"'http://lunach.ru/?cum=&url={link}&tpl=vk'"
        name = f"camshot{randomnumber}.jpg"
        os.system(f"wget -O {name} {url}")
        photo = self.uploadphoto(name)
        self.sendmsg(f"🌚🌚🌚", photo)
        os.remove(name)
