from vk_bot.core.utils.modutil import BacisPlug
import requests
class Convvalute(BacisPlug):
    doc = "Конвертер валют"
    command = ["/конвертер"]
    def main(self):
            api = "https://www.cbr-xml-daily.ru/daily_json.js"
            r = requests.get(api)
            encode = r.json()
            usd = encode["Valute"]["USD"]["Value"]
            eur = encode["Valute"]["EUR"]["Value"]
            try:
                val = float(self.text[1])
            except ValueError:
                self.sendmsg("Ты должен ввести цифру!\nНапример: /конвертер 5 usd")
            if val <= 0:
                self.sendmsg("Число должно быть больше 0!")
            elif self.text[2] == "usd":
                self.sendmsg(f"💰{'%g'%val}$:\nВ рублях: {round(val*usd, 3)}₽\nВ евро: {round(val*usd/eur, 3)}€")
            elif self.text[2] == "eur":
                self.sendmsg(f"💰{'%g'%val}€:\nВ рублях: {round(val*eur, 3)}₽\nВ долларах:{round(val*eur/usd, 3)}$")
            else:
                self.sendmsg("Выбери: usd или eur!\nНапример: /конвертер 5 usd")