from vk_bot.core.modules.basicplug import BasicPlug
from vk_bot import mods
from boltons import iterutils


class GetHelp(BasicPlug):
    doc = "Вызвать хелп"
    command = ["help", "хелп", "начать",
               "помощь", "команды", "старт", "начать"]

    def main(self):
        lhelp = []
        mhelp = "\n"
        allowedtype = ["command", "specialcommand"]
        for moduli in mods.modules:
            if moduli.types in allowedtype and moduli.available_for != "admins" and moduli.included:
                lhelp.append(dict(command=moduli.command, doc=moduli.doc))
        lhelp = list(iterutils.chunked_iter(lhelp, 11))
        lhelp = [dict(command="уходи от", doc="сюда мужик")] + lhelp
        try:
            number = int(self.text[1])
            lhelp2 = lhelp[number]
        except:
            number = 1
            lhelp2 = lhelp[1]
        mhelp += "Префиксы команд: / и ! , пример: !жив? или /жив? \n"
        for moduli in lhelp2:
            mhelp += f"• {', '.join(moduli['command'])} - {moduli['doc']} \n"
        mhelp += f"Страница: {number} \n"
        mhelp += f"Всего страниц: {len(lhelp)-1} \n"
        mhelp += "Пример переключения на другую страницу: /хелп 3"
        self.sendmsg(mhelp)
