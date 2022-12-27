from pyrogram import errors,enums
from datetime import datetime
from pyrogram import *
from gtts import gTTS
from utils import *
import configparser
import platform
import asyncio
import sqlite3
import sys

os.chdir(sys.path[0])

def restart():
    if str(platform.system()).lower() == 'linux':
        execl(sys.executable, 'python', __file__, *sys.argv[1:])
    elif str(platform.system()).lower() == 'windows':
        execl(sys.executable, 'python', __file__, *sys.argv[1:])
    exit()

stoponline=False
config = configparser.ConfigParser()
if not path.isfile('./settings.ini'):
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
    ''')
    print('Created config!\nFill api_id and api_hash')
    sys.exit()

config.read(r'./settings.ini')
api_id = config.get('main','api_id')
api_hash = config.get('main','api_hash')
app = Client('my_account',api_id=api_id, api_hash=api_hash)

#Settings
try:
    htext = Setting('htext',config.get('main','htext'))
    hideset = Setting('hide',config.get('main','hide'))
    autoreac = Setting('autoreac',config.get('main','autoreac'))
    ttsset = Setting('tts',config.get('main','tts'))
    jacset = Setting('jac',config.get('main','jac'))
    prefix = str(config.get('main','prefix'))
    #Settings dict
    settings_list = {'htext':htext,'hide':hideset,'autoreac':autoreac,'tts':ttsset,'jac':jacset}
except configparser.NoOptionError as e:
    option = str(e)
    option_start = int(str(option).find("No option '"))+len("No option '")
    option_end = int(str(option).find("' in section"))
    config.set('main',str(option[option_start:option_end]), 'f')
    config.write(open('settings.ini','w'))
    print('Please wait we are creating settings for the config file')
    restart()
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
        await warn(app,msg,'Такой настройки нет!')
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
async def type_com(_, msg):
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

@app.on_message(filters.command('split', prefixes=prefix) & filters.me)
async def split_com(_,msg):
    try:text = str(msg.text).split(' ')[1:]
    except IndexError:await warn(app,msg,'Введите текст!')
    chat_id = msg.chat.id
    await msg.delete()
    conv_text = []

    async def send_frame():
        await app.send_message(chat_id,'<code>========</code>')

    await send_frame()

    for l in ' '.join(text):
        if l==' ':
            conv_text.append('ㅤ')
        elif l!=' ':
            conv_text.append(l)
    
    for t in conv_text:
        await app.send_message(chat_id,'<b>'+t+'</b>')

    await send_frame()

@app.on_message(filters.command('hackerstr', prefixes=prefix) & filters.me)
async def hackerstr_com(_,msg):
    try:
        lenght = msg.text.split(' ', maxsplit=1)[1]
    except IndexError:
        await warn(app,msg,'Введите длину сообщения!',False)
    else:
        try:
            await msg.edit(generatehackerstr(int(lenght)))
        except errors.MessageTooLong:
            await warn(app,msg,'Сообщение слишком длинное!',False)

@app.on_message(filters.command('like',prefixes=prefix) & filters.me)
async def like_com(_,msg):
    chat_id = msg.chat.id
    try:limit = str(msg.text).split(' ')[1]
    except IndexError:await warn(app,msg,'Введите лимит (10,100,etc)!');return None
    else:
        count=0
        await msg.delete()
        async for message in app.get_chat_history(chat_id):
            await app.send_reaction(chat_id,message.id,'👍')
            count+=1
            if count>=int(limit):
                break

@app.on_message(filters.command('spam', prefixes=prefix) & filters.me)
async def spam_com(_, msg):
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
async def tts_com(_, msg):
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
            await warn(app,msg,'Нет такого языка!',True)
        else:
            await msg.delete()        
            tts.save('voice.mp3')
            await app.send_voice(msg.chat.id,'voice.mp3')

@app.on_message(filters.command('hide', prefixes=prefix) & filters.me)
async def hide_com(_, msg):
    await msg.edit('||'+msg.text[4:]+'||')

#Misc
@app.on_message(filters.command('hack', prefixes=prefix) & filters.me)
async def hack_com(_, msg):
    user = msg.text.split(' ',maxsplit=1)[1]
    await msg.edit('Начинаю взлом...')
    await asyncio.sleep(1)
    for i in range(0,100+1,4):
        await msg.edit(str(i)+'%')
    await asyncio.sleep(0.6)
    await msg.edit(f'{user} успешно взломан!\nАйпи: {getrandomip()}\nГеолокация: {getrandomgeo()}\nHwid: {getrandomhwid()}')

@app.on_message(filters.command('rand',prefixes=prefix) & filters.me)
async def rand_com(_,msg):
    from random import randint
    try:
        nums = (msg.text).split(' ')[1:]
    except IndexError:
        await warn(msg,'Введите числа')
    try:
        await msg.edit('<code>'+str(randint(int(nums[0]),int(nums[1])))+'</code>')
    except ValueError:
        await warn(app,msg,'Второе число должно быть не больше первого.',False)

@app.on_message(filters.command('count',prefixes=prefix) & filters.me)
async def count_com(_,msg):
    await count_anim(msg)

@app.on_message(filters.command('rsky',prefixes=prefix) & filters.me)
async def rsky_com(_,msg):
    await usky(msg)

@app.on_message(filters.command('jac',prefixes=prefix) & filters.me)
async def jac_com(_,msg):
    await jac_img(app,msg)

@app.on_message(filters.command('meme',prefixes=prefix) & filters.me)
async def meme_com(_,msg):
    try:category = str(msg.text).split(' ')[1]
    except IndexError:await warn(app,msg,','.join(umemes.keys()));return None
    try:meme = str(msg.text).split(' ')[2]
    except IndexError:
        try:umemes[str(category).lower()]
        except KeyError:await warn(app,msg,','.join(umemes.keys()));return None
        await warn(app,msg,','.join([m.getname() for m in umemes[str(category).lower()]]));return None
    else:
        await msg.delete()
        for memas in umemes[str(category).lower()]:
            if meme.capitalize() == memas.getname():
                await memas.send(app,msg)
                break

@app.on_message(filters.command('math', prefixes=prefix) & filters.me)
async def math_com(_,msg):
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
async def help_com(_, msg):
    settings = [str(i[0])+' ' for i in settings_list.items()]

    code = lambda text : '<code>'+text+'</code>'
    bold = lambda text : '<bold>'+text+'</bold>'

    help_list = []
    class Command:

        def __init__(self,name,args,desc,reply=False):
            self.name = name
            self.args = args
            self.desc = desc
            self.reply = reply
            
            args_to_add = []
            
            
            if args==None:
                args_to_add = []
            elif args!=None:
                for arg in args:
                    args_to_add.append('('+arg+')')
            if not reply:
                help_list.append(str(code(prefix+name)+' '+code(' '.join(args_to_add))+' - '+code(desc)))
            elif reply:
                help_list.append(str(code(prefix+name)+' '+code('-> Вы должны ответить на сообщение! ')+' '+code(' '.join(args_to_add))+' - '+code(desc)))
    Command('profile',None,'показывает профиль пользователя, если написать в ответ на сообщение другого пользовЫателя можно также увидеть его профиль')
    Command('type',['текст'],'анимация текста')
    Command('hide',['текст'],'скрытый текст')
    Command('hackerstr',['текст'],'строка с разными символами')
    Command('hack',['пользователь'],'"взламывает" пользователя')
    Command('spam',['количество','текст'],'спамит сообщениями')
    Command('tts',['в какой язык [en,ru,etc]','текст'],'отправляет голосовое сообщение с текстом')
    Command('rand',['первое число','второе число'],'генерирует рандомное число')
    Command('math',['первое число','оператор [+,-,/]','второе число'],'математика')
    Command('count',None,'считает 1000-1')
    Command('rsky',None,'делает симуляцию разноцветного неба')
    Command('jac',['текст'],'цитата Жака Фреско')
    Command('meme',['мем'],'отправляет мем')
    Command('like',['лимит'],'лайкает сообщения')
    Command('split',['текст'],'делает из текста, куча сообщений с 1 символом')
    Command('ню',None,'пересылает сообщение в облако',True)
    Command('action',['действие'],'выполняет действие')
    Command('python',['eval expression'],'выполняет python-код')
    Command('getmsg',None,'выводит данные сообщения в консоль',True)
    Command('stop',None,'останавливает процесс, например, когда ключена команда .count')
    Command('del',None,'удаляет сообщение',True)
    Command('update',None,'обновляет юзер бота с GitHub-репозитория')
    Command('online',None,'делает вас всегда в сети')
    Command('offline',None,'останавливает команду .online')
    Command('prefix',['новый префикс'],'меняет префикс')
    Command('restart',None,'перезапускает юзер бота')
    Command('info',None,'информация об юзер боте')
    Command('quit',None,'выходит из юзер бота')
    print(help_list)

    await msg.edit(bold("-- PyUserBot's help menu --")+'\n'+'\n'.join(help_list))
@app.on_message(filters.command('stop',prefixes=prefix) & filters.me)
async def stop_com(_,msg):
    changestop(True)
    await msg.delete()

@app.on_message(filters.command('info',prefixes=prefix) & filters.me)
async def info_com(_,msg):
    chat_id = msg.chat.id
    await msg.delete()
    lines_files = ['userbot.py','utils.py','main.py']
    lines = 0
    for file in lines_files:
        with open(file,'r',encoding='cp1251',errors='ignore') as py_file:
            data = py_file.read()
            data = data.split('\n')
            lines+=len(data)
    await app.send_message(chat_id,f'''
В юзерботе {str(lines)} строчек кода
<a href="https://github.com/purpl3-yt/pyuserbot">Код юзербота</a>''',disable_web_page_preview=True)


@app.on_message(filters.command('python',prefixes=prefix) & filters.me)
async def python_com(_,msg):
    run = str(msg.text).split(' ')[1:]
    eval_output = eval(' '.join(run))

    await msg.edit(eval_output)

@app.on_message(filters.command('prefix',prefixes=prefix) & filters.me)
async def prefix_com(_,msg):
    try:new_prefix = str(msg.text).split(' ')[1]
    
    except IndexError:
        await warn(app,msg,'Введите новый префикс.')
    
    else:
        prefix = str(new_prefix)

        config.set('main','prefix',str(new_prefix))
        config.write(open('settings.ini','w'))

        await warn(app,msg,'Сохранён новый префикс, перезапускаюсь...')

        if str(platform.system()).lower() == 'linux':
            execl(sys.executable, 'python', __file__, *sys.argv[1:])
        elif str(platform.system()).lower() == 'windows':
            execl(sys.executable, 'python', __file__, *sys.argv[1:])
        exit()

@app.on_message(filters.command('del',prefixes=prefix) & filters.me)
async def delete_com(_,msg):
    if msg.from_user.is_self==True:
        await app.delete_messages(msg.chat.id,msg.reply_to_message_id)
        await msg.delete()
    elif msg.from_user.is_self==False:
        await warn(app,msg,'Это не ваше сообщение.',False)
@app.on_message(filters.command('getmsg',prefixes=prefix) & filters.me)
async def getmsg_com(_,msg):
    print(msg)
    await warn(app,msg,'Данные выведены в консоль.',False)

@app.on_message(filters.command('online',prefixes=prefix) & filters.me)
async def online_com(_,msg):
    global stoponline
    await warn(app,msg,'Always Online')
    while True:
        if stoponline==False:
            online = await app.send_message('me','.')
            await app.delete_messages('me', online.id)
            await asyncio.sleep(10)
        elif stoponline==True:
            stoponline=False
            break
@app.on_message(filters.command('offline',prefixes=prefix) & filters.me)
async def offline_com(_,msg):
    global stoponline
    await warn(app,msg,'Постоянный онлайн выключен.')
    stoponline=True

@app.on_message(filters.command('test', prefixes=prefix) & filters.me)
async def test_com(_,msg):
    await warn(app,msg,'TEST COMMAND!!!!')

@app.on_message(filters.command('action',prefixes=prefix) & filters.me)
async def action_com(_,msg):
    chat_id = msg.chat.id

    actions = {
        'video':enums.ChatAction.RECORD_VIDEO,
        'audio':enums.ChatAction.RECORD_AUDIO,
        'sticker':enums.ChatAction.CHOOSE_STICKER,
        'contact':enums.ChatAction.CHOOSE_CONTACT,
        'play':enums.ChatAction.PLAYING,
        'type':enums.ChatAction.TYPING,
        'upload_audio':enums.ChatAction.UPLOAD_AUDIO,
        'upload_video':enums.ChatAction.UPLOAD_VIDEO,
        'upload_document':enums.ChatAction.UPLOAD_DOCUMENT,
        'cancel':enums.ChatAction.CANCEL}
    try:mode = str(str(msg.text).split(' ')[1]).lower()
    except IndexError:await warn(app,msg,'Выберите режим! '+', '.join(list(actions.keys())));return None
    else:
        await msg.delete()
        await app.send_chat_action(chat_id,actions[mode])

        await sleep(random.randint(30,60))

@app.on_message(filters.command('update',prefixes=prefix) & filters.me)
async def update_com(_,msg):
    await msg.edit('<code>Обновляюсь...</code>')
    check_version(True)
    await warn(app,msg,'Обновление прошло успешно, напишите .restart для перезагрузки.')

@app.on_message(filters.command('restart',prefixes=prefix) & filters.me)
async def restart_com(_,msg):
    await warn(app,msg,'Перезагружаюсь, подождите пару секунд...')

    restart()

@app.on_message(filters.command('ню',prefixes=prefix) & filters.me)
async def ny_com(_,msg):
    try:
        await app.delete_messages(msg.chat.id,msg.id)
        await app.forward_messages('me',msg.chat.id,msg.reply_to_message.id)
    except AttributeError:
        await app.delete_messages(msg.chat.id,msg.id)

@app.on_message(filters.command('quit',prefixes=prefix) & filters.me)
async def quit_com(_,msg):
    await warn(app,msg,'Выключаюсь...')

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
    print(f'By: https://t.me/PLNT_YT\nYour system is: {str(platform.system())}\nStarted at: '+datetime.now().strftime('%m/%d/%Y - %H:%M'))
    try:
        app.run()

    except sqlite3.OperationalError:
        if str(platform.system()).lower() == 'linux':
            print('\n\nYou have sqlite3 error!\nEnter: "fuser my_account.session"\nAnd check number at end\nAnd type: "kill -9 <number in command fuser>"\n\n')
        elif str(platform.system()).lower() == 'windows':
            print('\n\nYou have sqlite3 error!\nOpen cmd and enter: taskkill /F /IM python.exe\n\n')
run()
