from vk_bot.core.utils.modutil import BacisPlug
import random
class Answer(BacisPlug):
    doc = "Ответы на заданные сообщения"
    command = ["споки", "спокойной", "привет", "ку", "зиг", "слава украине", 'драсте']
    def main(self):
        zapros = self.text[0].lower()
        if zapros == "споки" or zapros == "спокойной":
            answer = ["Спотьки", "Спокойной ночи", "Спи, но я приду и выебу тебя историей аир"
                    ,"Сладких снов", "Эротишных снов🌚🌚🌚"]
        elif zapros == "слава украине":
            answer = "🇺🇦героям слава🇺🇦"
        else:
            answer = ["Кук", "зиг хайль", "куку нахуй",
                    "🇺🇦слава украине🇺🇦", "здравствуй", "здравия желаю"]
        self.sendmsg(random.choice(answer))