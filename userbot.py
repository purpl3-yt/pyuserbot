import asyncio
from os import execl, path
import platform
import sqlite3
import sys
from pyrogram import *
from pyrogram import errors
from utils import *
import configparser

os.chdir(sys.path[0])

stoponline=False
config = configparser.ConfigParser()
if not path.isfile('./settings.ini'):
    newconfig = open('settings.ini', 'w')
    newconfig.write('[main]\napi_id = 123123\napi_hash = abcdefg1234\n')
    newconfig.close()
    print('Created new empty config, please check root dir')
    sys.exit()
config.read(r'./settings.ini')
api_id = config.get('main','api_id')
api_hash = config.get('main','api_hash')
app = Client('my_account',api_id=api_id, api_hash=api_hash)

if not os.path.isfile('./settings.ini'):
    with open('settings.ini','w') as cfg:
        cfg.write('''
[main]
api_id = ???
api_hash = ???
prefix = .
htext = f
hide = f
autoreac = f
tts = f
jac = f
font = f
oleg = f
''')
    print('Created config!\nFill api_id and api_hash')

prefix = str(config.get('main','prefix'))

#Settings
try:
    htext = Setting('htext',config.get('main','htext'))
    hideset = Setting('hide',config.get('main','hide'))
    autoreac = Setting('autoreac',config.get('main','autoreac'))
    ttsset = Setting('tts',config.get('main','tts'))
    jacset = Setting('jac',config.get('main','jac'))
    olegset = Setting('oleg',config.get('main','oleg'))
    #Settings dict
    settings_list = {'htext':htext,'hide':hideset,'autoreac':autoreac,'tts':ttsset,'jac':jacset,'oleg':olegset}
except configparser.NoOptionError as e:
    from pathlib import Path
    option = str(e)
    option_start = int(str(option).find("No option '"))+len("No option '")
    option_end = int(str(option).find("' in section"))
    config.set('main',str(option[option_start:option_end]), 'f')
    config.write(open('settings.ini','w'))
    print('Please wait we are creating settings for the config file')
    if str(platform.system()).lower() == 'linux':
        execl(sys.executable, 'python', __file__, *sys.argv[1:])
        exit()
    elif str(platform.system()).lower() == 'windows':
        execl(sys.executable, 'python', __file__, *sys.argv[1:])
        exit()
stop=False
#System
@app.on_message(filters.command('set', prefixes=prefix) & filters.me)
async def set(_, msg):
    try:
        what = msg.text.split(' ')[1]
    except IndexError:
        settings = []
        for i in settings_list.keys():
            settings.append(settings_list.get(i).getname()+': '+settings_list.get(i).getstatus())
        await msg.edit(f'Все настройки: <code>{", ".join(settings)}</code>')
        return None
    try:
        status = msg.text.split(' ')[2]
    except IndexError:
        await warn(app,msg,'Введите статус: (t,f) t - вкл f - выкл')
        return None
    try:
        if not status in ['t','f']:
            await warn(app,msg,'Введите статус: (t,f) t - вкл f - выкл')
            return None
        config.set('main',str(what),str(status))
        config.write(open('settings.ini','w'))
        set = settings_list[what]
        set.setstatus(status)

    except KeyError:
        await warn(app,msg,'Такой настройки нету!')
    else:
        try:
            await warn(app,msg,f'Настройка {what} успешно сохранена!',False)
        except IndexError:
            await warn(app,msg,'Введите настройку')
@app.on_message(filters.command('profile', prefixes=prefix) & filters.me)
async def profile(_,msg):
    await getprofile(msg)
#Commands
#Messages
@app.on_message(filters.command('type', prefixes=prefix) & filters.me)
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

@app.on_message(filters.command('hackerstr', prefixes=prefix) & filters.me)
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

@app.on_message(filters.command('spam', prefixes=prefix) & filters.me)
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

@app.on_message(filters.command('tts', prefixes=prefix) & filters.me)
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

@app.on_message(filters.command('hide', prefixes=prefix) & filters.me)
async def hide(_, msg):
    await msg.edit('||'+msg.text[4:]+'||')

#Misc
@app.on_message(filters.command('hack', prefixes=prefix) & filters.me)
async def hack(_, msg):
    user = msg.text.split(' ',maxsplit=1)[1]
    await msg.edit('Начинаю взлом...')
    await asyncio.sleep(1)
    for i in range(0,100+1,4):
        await msg.edit(str(i)+'%')
    await asyncio.sleep(0.6)
    await msg.edit(f'{user} успешно взломан!\nАйпи: {getrandomip()}\nГеолокация: {getrandomgeo()}\nHwid: {getrandomhwid()}')

@app.on_message(filters.command('rand',prefixes=prefix) & filters.me)
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

@app.on_message(filters.command('ghoul',prefixes=prefix) & filters.me)
async def ghoul(_,msg):
    await ghoul_anim(msg)

@app.on_message(filters.command('rsky',prefixes=prefix) & filters.me)
async def rsky(_,msg):
    await usky(msg)

@app.on_message(filters.command('jac',prefixes=prefix) & filters.me)
async def jac(_,msg):
    await jac_img(app,msg)

@app.on_message(filters.command('meme',prefixes=prefix) & filters.me)
async def meme_command(_,msg):
    try:mem = str(msg.text).split(' ')[1]
    except IndexError:await warn(app,msg,','.join(umemes));return None
    await meme(app,msg,mem)
    await msg.delete()

@app.on_message(filters.command('олег', prefixes=prefix) & filters.all)
async def oleg(_,msg):
    if olegset.getstatus() == 't':
        await meme(app,msg,'oleg')

@app.on_message(filters.command('math', prefixes=prefix) & filters.me)
async def math(_,msg):
    try:num1 = str(msg.text).split(' ')[1]
    except IndexError:await warn(app,msg,'Введите первое число!')
    try:operation = str(msg.text).split(' ')[2]
    except IndexError:await warn(app,msg,'Введите операцию! [+,-,/,*]')
    try:num2 = str(msg.text).split(' ')[3]
    except IndexError:await warn(app,msg,'Введите второе число!')
    else:
        await umath(msg,num1,operation,num2)

#Help
@app.on_message(filters.command('help', prefixes=prefix) & filters.me)
async def help(_, msg):
    settings = [str(i[0])+' ' for i in settings_list.items()]
    await msg.edit(f'''<code>
Доступные команды:
.set (настройка) (статус) - меняет настройки
Настройки: {' '.join(settings)}
.profile - показывает профиль пользователя, если написать команду в ответ другому юзеру выведет его инфу
.type (текст) - делает анимацию текста
.hide (текст) - делает текст спойлером
.hackerstr (текст) - делает строку с разными символами
.hack (пользователь) - "взламывает" пользователя
.spam (количество) (текст) - спамит сообщениями
.tts (в какой язык [en,ru,etc]) (текст) - отправляет голосовое сообщение с текстом
.rand (первое число) (второе число) - генерирует рандомное число
.math (первое число) (оператор [+,-,/]) (второе число)
.ghoul - считает 1000-1 #deadinside
.rsky - делает разноцветное небо
.jac (текст) - делает цитату жака фреско
.meme (мем) - отправляет мем
.олег - отправляет олега
.stop - останавливает процесс, например когда ключена команда .ghoul
.del -> Вы должны ответить на сообщение! - удаляет сообщение
.getmsg -> Вы должны ответить на сообщение! - выводит данные сообщения в консоль
.ню -> Вы должны ответить на сообщение! - пересылает сообщение в облако
.python (eval expression) - выполняет код пайтона
.prefix (новый префикс) - меняет префикс
.online - Делает вас всегда в онлайне
.offline - Останавливает команду .online
.update - обновляет юзер бота
.restart - перезапускает юзер бота
.quit - выходит из юзер бота</code>
''')
@app.on_message(filters.command('stop',prefixes=prefix) & filters.me)
async def stop(_,msg):
    changestop(True)
    await msg.delete()

@app.on_message(filters.command('python',prefixes=prefix) & filters.me)
async def python(_,msg):
    run = str(msg.text).split(' ')[1:]
    eval_output = eval(' '.join(run))

    await msg.edit(eval_output)

@app.on_message(filters.command('prefix',prefixes=prefix) & filters.me)
async def prefix_com(_,msg):
    try:new_prefix = str(msg.text).split(' ')[1]
    
    except IndexError:
        await warn(app,msg,'Введите новый префикс!')
    
    else:
        prefix = str(new_prefix)

        config.set('main','prefix',str(new_prefix))
        config.write(open('settings.ini','w'))

        await warn(app,msg,'Сохранен новый префикс! Перезапуск юзер бота!')

        if str(platform.system()).lower() == 'linux':
            execl(sys.executable, 'python', __file__, *sys.argv[1:])
        elif str(platform.system()).lower() == 'windows':
            execl(sys.executable, 'python', __file__, *sys.argv[1:])
        exit()

@app.on_message(filters.command('del',prefixes=prefix) & filters.me)
async def delete(_,msg):
    if msg.from_user.is_self==True:
        await app.delete_messages(msg.chat.id,msg.reply_to_message_id)
        await msg.delete()
    elif msg.from_user.is_self==False:
        await warn(app,msg,'Это не ваше сообщение!',False)
@app.on_message(filters.command('getmsg',prefixes=prefix) & filters.me)
async def getmsg(_,msg):
    print(msg)
    await warn(app,msg,'Данные выведены в консоль',False)

@app.on_message(filters.command('online',prefixes=prefix) & filters.me)
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
@app.on_message(filters.command('offline',prefixes=prefix) & filters.me)
async def offline(_,msg):
    global stoponline
    await warn(app,msg,'Перестаём быть в онлайне!')
    stoponline=True

@app.on_message(filters.command('update',prefixes=prefix) & filters.me)
async def update(_,msg):
    await msg.edit('<code>Обновление юзер бота!</code>')
    check_version(True)
    await warn(app,msg,'Обновление успешно завершено! напишите команду .restart для перезагрузки')

@app.on_message(filters.command('restart',prefixes=prefix) & filters.me)
async def restart(_,msg):
    await warn(app,msg,'Перезагрузка юзер бота! подождите 5-10 секунд')
    if str(platform.system()).lower() == 'linux':
        execl(sys.executable, 'python', __file__, *sys.argv[1:])
    elif str(platform.system()).lower() == 'windows':
        execl(sys.executable, 'python', __file__, *sys.argv[1:])
    exit()

@app.on_message(filters.command('ню',prefixes=prefix) & filters.me)
async def ny(_,msg):
    try:
        await app.delete_messages(msg.chat.id,msg.id)
        await app.forward_messages('me',msg.chat.id,msg.reply_to_message.id)
    except AttributeError:
        await app.delete_messages(msg.chat.id,msg.id)

@app.on_message(filters.command('quit',prefixes=prefix) & filters.me)
async def quit_com(_,msg):

    await warn(app,msg,'Выключаем юзер бота!')

    quit()

#On messages
@app.on_message(filters.all | filters.me | filters.private)
async def write_self(_,msg):
    if msg.from_user!=None:
        global htext,hideset,tts
        if msg.from_user.is_self == True:
            if str(htext.getstatus()).lower()=='t':
                while True:
                    for i in text_animation(msg.text):
                        await msg.edit(i)
                        tbp = i
                        await asyncio.sleep(0.03)
                    break
            elif str(hideset.getstatus()).lower()=='t':
                await msg.edit('||'+msg.text[4:]+'||')
            elif str(ttsset.getstatus()).lower()=='t':
                if msg.text!=None:
                    from gtts import gTTS
                    text = str(msg.text).split(' ')[0:]
                    voicetts = gTTS(str(' '.join(text)),lang='ru')
                    await msg.delete()        
                    voicetts.save('voice.mp3')
                    await app.send_voice(msg.chat.id,'voice.mp3')
            elif str(jacset.getstatus()).lower()=='t':
                await jac_img(app,msg,True)
        elif msg.from_user.is_self == False:
            if str(autoreac.getstatus()).lower()=='t':
                from random import choice
                random_emoji = ['🔥','👍']
                await app.send_reaction(msg.chat.id, msg.id, choice(random_emoji))
def run():#Run userbot
    print(getlogo(),end='')
    print(f'By: https://t.me/PLNT_YT\nYour system is: {str(platform.system())}')
    try:
        app.run()
    except sqlite3.OperationalError as e:
        if str(platform.system()).lower() == 'linux':
            print('\n\nYou have sqlite3 error!\nEnter: "fuser my_account.session"\nAnd check number at end\nAnd type: "kill -9 <number in command fuser>"\n\n')
        elif str(platform.system()).lower() == 'windows':
            print('\n\nYou have sqlite3 error!\nOpen cmd and enter: taskkill /F /IM python.exe\n\n')
run()
