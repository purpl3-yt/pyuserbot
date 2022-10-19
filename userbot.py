import asyncio
import os
import sys
from pyrogram import *
from pyrogram import errors
from utils import *
import configparser
stoponline=False
config = configparser.ConfigParser()
if not os.path.isfile('./settings.ini'):
    newconfig = open('settings.ini', 'w')
    newconfig.write('[main]\napi_id = 123123\napi_hash = abcdefg1234')
    newconfig.close()
    print('Created new empty config, please check root dir')
    sys.exit()
config.read(r'./settings.ini')
api_id = config.get('main','api_id')
api_hash = config.get('main','api_hash')
app = Client('my_account',api_id=api_id, api_hash=api_hash)
#Settings
htext = Setting('htext','f')
hideset = Setting('hide','f')
autoreac = Setting('autoreac','f')
ttsset = Setting('tts','f')
settings_list = {'htext':htext,'hide':hideset,'autoreac':autoreac,'tts':ttsset}
stop=False
#System
@app.on_message(filters.command('set', prefixes='.') & filters.me)
async def set(_, msg):
    try:
        what = msg.text.split(' ')[1]
    except IndexError:
        settings = [str(i) for i in settings_list.keys()]
        await msg.edit(f'Все настройки: <code>{",".join(settings)}</code>')
        return None
    try:
        status = msg.text.split(' ')[2]
    except IndexError:
        await warn(app,msg,'Введите статус: (t,f) t - вкл f - выкл')
        return None
    try:
        set = settings_list[what]
        set.setstatus(status)
    except KeyError:
        await warn(app,msg,'Такой настройки нету!')
    else:
        try:
            await warn(app,msg,f'Настройка {what} успешно сохранена!',False)
        except IndexError:
            await warn(app,msg,'Введите настройку')
@app.on_message(filters.command('profile', prefixes='.') & filters.me)
async def profile(_,msg):
    await getprofile(msg)
#Commands
#Messages
@app.on_message(filters.command('type', prefixes='.') & filters.me)
async def type(_, msg):
    orig_text = msg.text.split(' ', maxsplit=1)[1]
    tbp = ''
    while True:
        for i in text_animation(orig_text):
            try:
                await msg.edit(i+'</b>')
            except FloodWait as wait:
                await asyncio.sleep(0.05)
            tbp = i
            await asyncio.sleep(0.05)
        break

@app.on_message(filters.command('hackerstr', prefixes='.') & filters.me)
async def hackerstr(_,msg):
    try:
        lenght = msg.text.split(' ', maxsplit=1)[1]
    except IndexError:
        await warn(app,msg,'Введите длину сообщения!',False)
    else:
        try:
            await msg.edit(generatehackerstr(int(lenght)))
        except errors.MessageTooLong:
            await warn(app,msg,'Ваше сообщение слишком длинное!',False)

@app.on_message(filters.command('spam', prefixes='.') & filters.me)
async def spam(_, msg):
    await msg.delete()
    try:
        spam_count = msg.text.split(' ')[1]
        spam_data = msg.text.split(' ')[2:]
        for i in range(0,int(spam_count)):
            await app.send_message(int(msg.chat.id),text=' '.join(spam_data))
    except IndexError:
        await msg.edit('Введите данные (.spam 10 Hello!)')
        await asyncio.sleep(2)
        await msg.delete()

@app.on_message(filters.command('tts', prefixes='.') & filters.me)
async def tts(_, msg):
    from gtts import gTTS
    try:lang = str(msg.text).split(' ')[1]
    except IndexError:
        await warn(app,msg,'Введите язык (en,ru,etc.)')
    try:warntext = str(msg.text).split(' ')[2]
    except IndexError:await warn(app,msg,'Введите текст!')
    else:
        text = str(msg.text).split(' ')[2:]
        try:
            tts = gTTS(str(' '.join(text)),lang=lang)
        except ValueError:
            await warn(app,msg,'Такого языка нету!',True)
        else:
            await msg.delete()        
            tts.save('voice.mp3')
            await app.send_voice(msg.chat.id,'voice.mp3')


@app.on_message(filters.command('hide', prefixes='.') & filters.me)
async def hide(_, msg):
    await msg.edit('||'+msg.text[4:]+'||')

#Misc
@app.on_message(filters.command('hack', prefixes='.') & filters.me)
async def hack(_, msg):
    user = msg.text.split(' ',maxsplit=1)[1]
    await msg.edit('Начинаю взлом...')
    await asyncio.sleep(1)
    for i in range(0,100+1,4):
        await msg.edit(str(i)+'%')
    await asyncio.sleep(0.6)
    await msg.edit(f'{user} успешно взломан!\nАйпи: {getrandomip()}\nГеолокация: {getrandomgeo()}\nHwid: {getrandomhwid()}')

@app.on_message(filters.command('rand',prefixes='.') & filters.me)
async def rand(_,msg):
    from random import randint
    try:
        nums = (msg.text).split(' ')[1:]
    except IndexError:
        await warn(msg,'Введите числа')
    try:
        await msg.edit('<code>'+str(randint(int(nums[0]),int(nums[1])))+'</code>')
    except ValueError:
        await warn(app,msg,'Укажите 2 число не больше первого!',False)

@app.on_message(filters.command('ghoul',prefixes='.') & filters.me)
async def ghoul(_,msg):
    await ghoul_anim(msg)

@app.on_message(filters.command('rsky',prefixes='.') & filters.me)
async def rsky(_,msg):
    await usky(msg)

@app.on_message(filters.command('math', prefixes='.') & filters.me)
async def math(_,msg):
    try:num1 = str(msg.text).split(' ')[1]
    except IndexError:await warn(app,msg,'Введите первое число!')
    try:operation = str(msg.text).split(' ')[2]
    except IndexError:await warn(app,msg,'Введите операцию! [+,-,/]')
    try:num2 = str(msg.text).split(' ')[3]
    except IndexError:await warn(app,msg,'Введите второе число!')
    await umath(msg,num1,operation,num2)

#Help
@app.on_message(filters.command('help', prefixes='.') & filters.me)
async def help(_, msg):
    settings = [str(i[0])+' ' for i in settings_list.items()]
    await msg.edit(f'''
```
Доступные команды:
.setting (настройка) (статус) - меняет настройки
Настройки: {' '.join(settings)}
.profile - показывает профиль пользователя, если написать команду в ответ другому юзеру выведет его инфу
.type (текст) - делает анимацию текста
.hide (текст) - делает текст спойлером
.hackerstr (текст) - делает строку с разными символами
.hack (пользователь) - "взламывает" пользователя
.spam (количество) (текст) - спамит сообщениями
.tts (в какой язык [en,ru,etc]) (текст) - отправляет голосовое сообщение с текстом
.rand (первое число) (второе число) - генерирует рандомное число
.ghoul - считает 1000-7
.rsky - делает разноцветное небо
.stop - останавливает процесс, например когда ключена команда .ghoul
.del -> Вы должны ответить на сообщение! - удаляет сообщение
.getmsg -> Вы должны ответить на сообщение! - выводит данные сообщения в консоль
.online - Делает вас всегда в онлайне
.offline - Перестает быть в онлайне
.update - обновляет юзер бота```
''')
@app.on_message(filters.command('stop',prefixes='.') & filters.me)
async def stop(_,msg):
    changestop(True)
    await msg.delete()

@app.on_message(filters.command('del',prefixes='.') & filters.me)
async def delete(_,msg):
    if msg.from_user.is_self==True:
        await app.delete_messages(msg.chat.id,msg.reply_to_message_id)
        await msg.delete()
    elif msg.from_user.is_selfz==False:
        await warn(app,msg,'Это не ваше сообщение!',False)
@app.on_message(filters.command('getmsg',prefixes='.') & filters.me)
async def getmsg(_,msg):
    print(msg)
    await warn(app,msg,'Данные выведены в консоль',False)

@app.on_message(filters.command('online',prefixes='.') & filters.me)
async def online(_,msg):
    global stoponline
    await warn(app,msg,'Always Online')
    while True:
        if stoponline==False:
            online = await app.send_message('me','.')
            await app.delete_messages('me', online.id)
            await asyncio.sleep(45)
        elif stoponline==True:
            stoponline=False
            break
@app.on_message(filters.command('offline',prefixes='.') & filters.me)
async def offline(_,msg):
    global stoponline
    await warn(app,msg,'Перестаём быть в онлайне!')
    stoponline=True

@app.on_message(filters.command('update',prefixes='.') & filters.me)
async def update(_,msg):
    await msg.edit('Обновление юзер бота!')
    check_version(True)
    await msg.edit('Обновление успешно завершено! перезапустите юзербота')

#On messages
@app.on_message(filters.all & filters.private & filters.me)
async def write_self(_,msg):
    if msg.from_user!=None:
        global htext,hideset,tts
        if msg.from_user.is_self == True:
            if str(htext.getstatus()).lower()=='t':
                    if str(msg.text).lower() == '.set htext f':htext.setstatus('t')
                    elif str(msg.text).lower() == '.set htext t':htext.setstatus('f')
                    else:
                        while True:
                            for i in text_animation(msg.text):
                                await msg.edit(i)
                                tbp = i
                                await asyncio.sleep(0.03)
                            break
            elif str(hideset.getstatus()).lower()=='t':
                if str(msg.text).lower() == '.set hide f':hideset.setstatus('t')
                elif str(msg.text).lower() == '.set hide t':hideset.setstatus('f')
                else:await msg.edit('||'+msg.text[4:]+'||')
            elif str(ttsset.getstatus()).lower()=='t':
                if str(msg.text).lower() == '.set tts f':ttsset.setstatus('t')
                elif str(msg.text).lower() == '.set tts t':ttsset.setstatus('f')
                else:
                    from gtts import gTTS
                    text = str(msg.text).split(' ')[0:]
                    voicetts = gTTS(str(' '.join(text)),lang='ru')
                    await msg.delete()        
                    voicetts.save('voice.mp3')
                    await app.send_voice(msg.chat.id,'voice.mp3')
        elif msg.from_user.is_self == False:
            if str(autoreac.getstatus()).lower()=='t':
                if str(msg.text).lower() == '.set autoreac f':autoreac.setstatus('t')
                elif str(msg.text).lower() == '.set autoreac t':autoreac.setstatus('f')
                else:
                    from random import choice
                    random_emoji = ['🔥','👍','💩']
                    await app.send_reaction(msg.chat.id, msg.id, choice(random_emoji))


def run():#Run userbot
    print(getlogo(),end='')
    app.run()
run()