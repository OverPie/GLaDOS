from vk_bot.core.utils.modutil import BacisPlug
class Repeat(BacisPlug):
    doc = "Повторить сообщение"
    command = ["/повтори"]
    def main(self):
        text = " ".join(self.text[1:])
        self.sendmsg(text)