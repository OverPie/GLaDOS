import vk_api
from vk_api.utils import get_random_id
from vk_bot.core.sql.vksql import *

def relationmeet(text, vk, event):
    check = checkrelation('waitmeet', event.object.from_id)
    if check == None:
        check = checkrelation('relation', event.object.from_id)
        if check == None:
            userid = "".join(text[2][3:])
            userid = userid.split('|')[0]
            check = checkrelation('relation', userid)
            if check == None:
                check = checkrelation('waitmeet', userid)
                if check == None:
                    tableadd("waitmeet", "id, id2", (f"{event.object.from_id}, {userid}"))
                    vk.messages.send(user_id=int(userid), random_id=get_random_id(),
                                    message=f"*id{event.object.from_id}(Пользователь) предложил тебе встречаться!\nНапиши: '/отношения принять' или '/отношения отклонить'")
                else:
                    return "Этому пользователю уже кто-то предложил встречатся!"
            else:
                return "Этот пользователь уже встречается с кем-то!"
        else:
            return "Ай-яй-яй! Изменять нехорошо"
    else:
        return "Ты уже отправил приглашение!"
def reject(event, vk):
    check = checktable('waitmeet', 'id2', event.object.from_id)
    if check == None:
        return 'У тебя нет предложений встречаться!'
    else:
        userid = checktable('waitmeet', 'id2', event.object.from_id)
        vk.messages.send(user_id=int(userid['id']), random_id=get_random_id(),
                            message=f"*id{event.object.from_id}(Пользователь) отклонил твое предложение :()")
        tablerm('waitmeet', "id2", event.object.from_id)  
        return "Вы отклонили предложение"

def accept(event, vk):
    check = checktable('waitmeet', 'id2', event.object.from_id)
    if check == None:
        return 'У тебя нет предложений встречаться!'
    else:
        relationaccept(event.object.from_id)
        tablerm('waitmeet', "id2", event.object.from_id)
        userid = checktable('relation', 'id2', event.object.from_id)
        vk.messages.send(user_id=int(userid['id']), random_id=get_random_id(),
                            message=f"*id{event.object.from_id}(Пользователь) принял твое предложение! Поздравляем!")
        return "Вы приняли предложение! Поздравляем!"
def test(event, vk, message, case):
    check = checkrelation('relation', event.object.from_id)
    if check == None:
        return {'message': 'Ты ни с кем не встречаешься :('}
    else:
        userid = checktable('relation', 'id', event.object.from_id)
        if userid == None:
            userid = checktable('relation', 'id2', event.object.from_id)
        if userid['id2'] == event.object.from_id:
            userid = f"*id{userid['id']}({vk.users.get(user_ids=userid['id'], name_case=case)[0]['first_name']})"
            return {'message':f"{message} {userid}"}
        elif userid['id'] == event.object.from_id:
            userid = f"*id{userid['id2']}({vk.users.get(user_ids=userid['id2'], name_case=case)[0]['first_name']})"
            return {'message':f"{message} {userid}"}

def relation(event, vk, text):
    try:
        if text[1] == "принять":
            return {"message": accept(event, vk)}
        elif text[1] == "отклонить":
            return {"message": reject(event, vk)}
        elif text[:2] == ['/отношения', 'встречаться']:
            return {"message": relationmeet(text, vk, event)}
    except IndexError:
        return test(event, vk, "Ты встречаешься с", "ins")