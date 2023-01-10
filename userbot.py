from pyrogram import errors, enums, Client
from datetime import datetime
from gtts import gTTS
from utils import *
import configparser
import subprocess
import platform
import asyncio
import sqlite3
import asyncio
import psutil
import sys
code = lambda text : '<code>'+text+'</code>'
bold = lambda text : '<b>'+text+'</b>'

def getUptime():
    return datetime.now().strftime('%d/%m/%Y - %H:%M')

def clear():
    if platform.system().lower() == 'windows':
        os.system('cls')
    else:
        os.system('clear')

clear()

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
    ''')
    print('Created config!\nFill api_id and api_hash')
    sys.exit()

config.read(r'./settings.ini')
print('Read config!')
api_id = config.get('main','api_id')
print('Get Api ID!')
api_hash = config.get('main','api_hash')
print('Get Api Hash!')
app = Client('pyuserbot',api_id=api_id, api_hash=api_hash, device_model='PyUserBot')
print('Create Client!')
del api_id,api_hash#For security
print('Deteled api_id and api_hash vars to security!')

#Settings
try:
    htext = Setting('htext',config.get('main','htext'))
    hideset = Setting('hide',config.get('main','hide'))
    autoreac = Setting('autoreac',config.get('main','autoreac'))
    ttsset = Setting('tts',config.get('main','tts'))
    skullset = Setting('skull',config.get('main','skull'))
    terminalset = Setting('terminal',config.get('main','terminal'))
    nospaceset = Setting('nospace',config.get('main','nospace'))
    prefix = str(config.get('main','prefix'))
except configparser.NoOptionError as e:
    option_start = int(str(e).find("No option '"))+len("No option '")
    option_end = int(str(e).find("' in section"))
    config.set('main',str(e)[option_start:option_end], 'f')
    config.write(open('settings.ini','w'))
    print('Please wait we are creating settings for the config file!')
    restart()

stop=False
try:love_words = str(requests.get('https://pastebin.com/raw/ZSk4qP1d').text).split('\n');print('Words for command "loveword" collected!')
except:love_words = ''

@app.on_message(filters.command('set', prefixes=prefix) & filters.me)
async def set(_, msg: types.Message):
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
            await warn(app,msg,f'Настройка {what} успешно сохранена!',mode='info')
        except IndexError:
            await warn(app,msg,'Введите настройку!')
@app.on_message(filters.command('profile', prefixes=prefix) & filters.me)
async def profile_com(_,msg: types.Message):
    await getprofile(msg)

@app.on_message(filters.command('type', prefixes=prefix) & filters.me)
async def type_com(_, msg: types.Message):
    orig_text = msg.text.split(' ', maxsplit=1)[1]
    tbp = ''
    while True:
        for i in text_animation(orig_text):
            try:
                await msg.edit(i+'</b>')
            except errors.FloodWait as wait:
                await asyncio.sleep(0.05)
            tbp = i
            await asyncio.sleep(0.05)
        break

@app.on_message(filters.command('split', prefixes=prefix) & filters.me)
async def split_com(_,msg: types.Message):
    try:text_to_check = str(msg.text).split(' ')[1]
    except IndexError:await warn(app,msg,'Введите текст!')
    text = str(msg.text).split(' ')[1:]
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

@app.on_message(filters.command('len',prefixes=prefix) & filters.me)
async def len_com(_,msg: types.Message):
    async def send():
        len_text = msg.text
        if msg.reply_to_message != None:
            len_text = msg.reply_to_message.text
        await msg.edit('<b>Длина текста: </b><code>'+str(len(' '.join(str(len_text).split(' ')[1:])))+'</code> <b>символов!</b>')
    
    if msg.reply_to_message != None:
        await send()
        return None
        
    try:text_to_check = str(msg.text).split(' ')[1]
    except IndexError:
        await warn(app,msg,'Введите текст!');return None
    else:
        await send()
@app.on_message(filters.command('hackerstr', prefixes=prefix) & filters.me)
async def hackerstr_com(_,msg: types.Message):
    try:
        lenght = msg.text.split(' ', maxsplit=1)[1]
    except IndexError:
        await warn(app,msg,'Введите длину сообщения!')
    else:
        try:
            await msg.edit(generatehackerstr(int(lenght)))
        except errors.MessageTooLong:
            await warn(app,msg,'Сообщение слишком длинное!')

@app.on_message(filters.command('reac',prefixes=prefix) & filters.me)
async def reac_com(_,msg: types.Message):

    try:limit = str(msg.text).split(' ')[1]
    except IndexError:await warn(app,msg,'Введите лимит!');return None

    try:emoji = str(msg.text).split(' ')[2]
    except IndexError:emoji = '👍' 

    try:chat = str(msg.text).split(' ')[3]
    except IndexError:chat = None

    chat_id = msg.chat.id
    await msg.delete()
    async for m in app.get_chat_history(chat_id,int(limit)):
        try:
            await app.send_reaction(chat_id,m.id,emoji)
        except errors.exceptions.bad_request_400.MessageNotModified:
            pass

@app.on_message(filters.command('tag',prefixes=prefix) & filters.me)
async def tag_all_com(_,msg: types.Message):
    users_choice = [
        'admin',
        'bot',
        'all'
    ]

    async def work(mode,msg,users):
        if mode.lower() == 'inmsg':
            await app.send_message(msg.chat.id,' '.join(users))
        elif mode.lower() == 'outmsg':
            for u in users:
                await app.send_message(msg.chat.id,u)

    try:who = str(msg.text).split(' ')[1]
    except IndexError:await warn(app,msg,'Введите кого тегать! '+', '.join(users_choice));return None
    try:mode = str(msg.text).split(' ')[2]
    except IndexError:await warn(app,msg,'Введите режим! '+', '.join(['inmsg','outmsg']));return None
    users = []
    msg2 = msg
    await msg.delete()
    if who.lower() == 'admin':
        async for m in app.get_chat_members(msg2.chat.id,filter=enums.ChatMembersFilter.ADMINISTRATORS):
            users.append('@'+str(m.user.username))

    elif who.lower() == 'bot':
        async for m in app.get_chat_members(msg2.chat.id,filter=enums.ChatMembersFilter.BOTS):
            users.append('@'+str(m.user.username))

    elif who.lower() == 'banned':
        async for m in app.get_chat_members(msg2.chat.id,filter=enums.ChatMembersFilter.BANNED):
            users.append('@'+str(m.user.username))

    elif who.lower() == 'all':
        async for m in app.get_chat_members(msg2.chat.id):
            users.append('@'+str(m.user.username))
            
    await work(mode,msg2,users)

@app.on_message(filters.command('spam', prefixes=prefix) & filters.me)
async def spam_com(_, msg: types.Message):
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
async def tts_com(_, msg: types.Message):
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
async def hide_com(_, msg: types.Message):
    await msg.edit('||'+msg.text[4:]+'||')

#Misc
@app.on_message(filters.command('hack', prefixes=prefix) & filters.me)
async def hack_com(_, msg: types.Message):
    try:user = msg.text.split(' ')[1]
    except IndexError:await warn(app,msg,'Введите пользователя!')
    await msg.edit('Начинаю взлом...')
    await asyncio.sleep(1)
    for i in range(0,100+1,4):
        await msg.edit(str(i)+'%')
    await asyncio.sleep(0.6)
    await msg.edit(f'{user} успешно взломан!\nАйпи: {getrandomip()}\nГеолокация: {getrandomgeo()}\nHWID: {getrandomhwid()}')

@app.on_message(filters.command('count',prefixes=prefix) & filters.me)
async def count_com(_,msg: types.Message):
    await count_anim(msg)

@app.on_message(filters.command('rsky',prefixes=prefix) & filters.me)
async def rsky_com(_,msg: types.Message):
    await usky(msg)

@app.on_message(filters.command('meme',prefixes=prefix) & filters.me)
async def meme_com(_,msg: types.Message):
    try:category = str(msg.text).split(' ')[1]
    except IndexError:await warn(app,msg,','.join(umemes.keys()),mode='info');return None
    try:meme = str(msg.text).split(' ')[2]
    except IndexError:
        try:umemes[str(category).lower()]
        except KeyError:await warn(app,msg,','.join(umemes.keys()));return None
        await warn(app,msg,','.join([m.getname() for m in umemes[str(category).lower()]]),mode='info');return None
    else:
        await msg.delete()
        for memas in umemes[str(category).lower()]:
            if meme.capitalize() == memas.getname():
                await memas.send(app,msg)
                break

@app.on_message(filters.command('math', prefixes=prefix) & filters.me)
async def math_com(_,msg: types.Message):
    try:num1 = str(msg.text).split(' ')[1]
    except IndexError:await warn(app,msg,'Введите первое число!')
    try:operation = str(msg.text).split(' ')[2]
    except IndexError:await warn(app,msg,'Введите операцию! [+,-,/,*]')
    try:num2 = str(msg.text).split(' ')[3]
    except IndexError:await warn(app,msg,'Введите второе число!')
    else:
        await umath(msg,num1,operation,num2)

@app.on_message(filters.command('random', prefixes=prefix) & filters.me)
async def random_com(_,msg: types.Message):
    random_items = [
        'location',
        'letter',
        'music']
    try:what = str(msg.text).split(' ')[1]
    except IndexError:await warn(app,msg,'Введите что вывести: '+' '.join(random_items),mode='info')
    else:

        chat_id = msg.chat.id
        await msg.delete()
        if str(what).lower() == 'location':
            await app.send_location(chat_id,getrandomgeo()[0],getrandomgeo()[1])
        elif str(what).lower() == 'letter':
            await app.send_message(chat_id,'Рандомный символ: '+bold(str(random.choice([l for l in string.ascii_letters]))))
        elif str(what).lower() == 'music':
            music_files = [m.id async for m in app.get_chat_history('@simplephonk') if m.audio!=None]
            await app.forward_messages(chat_id,'@simplephonk',random.choice(music_files))

#Help
@app.on_message(filters.command('help', prefixes=prefix) & filters.me)
async def help_com(_, msg: types.Message):
    settings = [str(i[0])+' ' for i in settings_list.items()]

    help_list = []

    help_list.append(bold('Настройки: ')+code(''.join(settings)))

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
                help_list.append(str(code(prefix+name)+' '+code(' '.join(args_to_add))+' - '+bold(desc))+'\n')
            elif reply:
                help_list.append(str(code(prefix+name)+' '+code('-> Вы должны ответить на сообщение! ')+' '+code(' '.join(args_to_add))+' - '+bold(desc))+'\n')
    
    Command('type',['текст'],'анимация текста')
    Command('hide',['текст'],'скрытый текст')
    Command('hackerstr',['текст'],'строка с разными символами')
    Command('hack',['пользователь'],'"взламывает" пользователя')
    Command('spam',['количество','текст'],'спамит сообщениями')
    Command('tts',['в какой язык [en,ru,etc]','текст'],'отправляет голосовое сообщение с текстом')
    Command('math',['первое число','оператор [+,-,/]','второе число'],'математика')
    Command('meme',['мем'],'отправляет мем')
    Command('reac',['лимит','эмодзи'],'ставит реакцию на сообщение')
    Command('tag',['кого','режим'],'тегает людей')
    Command('split',['текст'],'делает из текста, куча сообщений с 1 символом')
    Command('len',['текст'],'выводит длину текста (также вы можете ответить на сообщение)')
    Command('action',['действие'],'выполняет действие')
    Command('python',['eval expression'],'выполняет python-код')
    Command('profile',None,'показывает профиль пользователя, если написать в ответ на сообщение другого пользователя можно также увидеть его профиль')
    Command('count',None,'считает 1000-1')
    Command('rsky',None,'делает симуляцию разноцветного неба')
    Command('ню',None,'пересылает сообщение в облако',True)
    Command('getmsg',None,'выводит данные сообщения в консоль',True)
    Command('getusers',None,'получить информацию об пользователях в чате')
    Command('stop',None,'останавливает процесс, например, когда ключена команда .count')
    Command('popen',['команда'],'выполняет команду в терминале')
    Command('del',None,'удаляет сообщение',True)
    Command('update',None,'обновляет юзер бота с GitHub-репозитория')
    Command('online',None,'делает вас всегда в сети')
    Command('offline',None,'останавливает команду .online')
    Command('prefix',['новый префикс'],'меняет префикс')
    Command('restart',None,'перезапускает юзер бота')
    Command('info',None,'информация об юзер боте')
    Command('quit',None,'выходит из юзер бота')
    
    await msg.edit("<u>-- <a href='https://github.com/purpl3-yt/pyuserbot'>PyUserBot's</a> help menu --</u>"+'\n'+''.join(help_list),disable_web_page_preview=True)

@app.on_message(filters.command('stop',prefixes=prefix) & filters.me)
async def stop_com(_,msg: types.Message):
    changestop(True)
    await msg.delete()

@app.on_message(filters.command('info',prefixes=prefix) & filters.me)
async def info_com(_,msg: types.Message):
    chat_id = msg.chat.id
    await msg.delete()
    lines_files = ['userbot.py','utils.py','main.py']
    lines = 0
    count_commands = 0
    for file in lines_files:
        with open(file,'r',encoding='cp1251',errors='ignore') as py_file:
            data = py_file.read()
            data = data.split('\n')
            lines+=len(data)
            
            if file=='userbot.py':
                for line in data:
                    if line.find('@app.on_message(filters.command')!=-1:
                        count_commands+=1

    text = f'''
🐍 {bold("PyUserBot")}
🗒 Кол-во строчек кода: {bold(str(lines))}
⏳ Аптайм: {bold(str(getUptime()))}
⌨️ Префикс: {bold("«")}{code(prefix)}{bold("»")}
🖋 Всего команд: {bold(str(count_commands))}'''

    if platform.system().lower() == 'windows':
        text+=f'\n🖥 Система: {bold("Windows 🖼")}'
    elif platform.system().lower() == 'linux':
        text+=f'\n🖥 Система: {bold("Linux 🐧")}'

    text+='\n⚙️ <a href="https://github.com/purpl3-yt/pyuserbot">Код юзербота</a>'

    await app.send_animation(chat_id,'https://i.imgur.com/8fYJVyO.mp4',text)

@app.on_message(filters.command('getusers',prefixes=prefix) & filters.me)
async def get_users_com(_,msg: types.Message):
    await msg.edit(bold('ℹ️ Получение информации...'))
    admins = []
    try:
        async for m in app.get_chat_members(msg.chat.id,filter=enums.ChatMembersFilter.ADMINISTRATORS):
            admins.append(m)
    except errors.exceptions.bad_request_400.ChannelInvalid:
        await warn(app,msg,'Ошибка получения информации!');return None
    bots = []
    async for m in app.get_chat_members(msg.chat.id, filter=enums.ChatMembersFilter.BOTS):
        bots.append(m)
    
    admin_privileges = False
    
    try:
        banned = []
        async for m in app.get_chat_members(msg.chat.id, filter=enums.ChatMembersFilter.BANNED):
            admin_privileges = True
            banned.append(m)
    except errors.exceptions.bad_request_400.ChatAdminRequired:
        admin_privileges = False
        pass

    text = f'''
{bold("🤖 Ботов в чате: ")} {code(str(len(bots)))}
{bold("🔨 Админов в чате: ")} {code(str(len(admins)))}'''

    if admin_privileges:
        text+=f'\n{bold("🚫 Забаненных в чате: ")} {code(str(len(banned)))}'
    elif not admin_privileges:
        text+=f"\n{bold('😭 Не удалось получить список забаненных!')}"

    await msg.edit(text)

@app.on_message(filters.command('python',prefixes=prefix) & filters.me)
async def python_com(_,msg: types.Message):
    run = str(msg.text).split(' ')[1:]
    eval_output = eval(' '.join(run))

    await msg.edit(eval_output)

@app.on_message(filters.command('popen',prefixes=prefix) & filters.me)
async def popen_com(_,msg: types.Message):
    try:command = str(msg.text).split(' ')[1:]
    except IndexError:await warn(app,msg,'Введите команду!')
    else:

        if r'.*.session.*' in ' '.join(command):
            await warn(app,msg,'Не делайте ничего с .session файлами!');return None

        await msg.edit(bold('Выполняем команду: ')+code(' '.join(command)))
        p = subprocess.Popen(' '.join(command), stdout=subprocess.PIPE, shell=True,encoding='utf-8', errors='ignore')
        result = p.communicate()[0]
        if result=='':
            await warn(app,msg,'Вывода нету!')
            return None
        
        if len(result)>=3000:
            with open('result.txt','w',encoding='utf-8') as result_file:
                result_file.write(result)
            
            await app.send_document(msg.chat.id,'./result.txt',caption=bold('Вывод большой так что он будет файлом!'))
            await msg.delete()
            
            os.remove('./result.txt')

            return None

        await msg.edit('<code>'+result+'</code>')

@app.on_message(filters.command('prefix',prefixes=prefix) & filters.me)
async def prefix_com(_,msg: types.Message):
    global prefix
    try:new_prefix = str(msg.text).split(' ')[1]
    
    except IndexError:
        await warn(app,msg,'Введите новый префикс.')
    
    else:
        
        if len(new_prefix)>2:
            await warn(app,msg,'Префикс должен быть не больше 2 символов!')
            return None

        if not new_prefix in r'[^a-zA-Zа-я-А-Я1-90;{}_+=|<>\" \[ \] \: \' \, \(\) \s]':
            await warn(app,msg,'Такой префикс поставить нельзя!')
            return None

        prefix = str(new_prefix)

        config.set('main','prefix',str(new_prefix))
        config.write(open('settings.ini','w'))

        await warn(app,msg,'Сохранён новый префикс, перезапускаюсь...',mode='info')

        restart()

@app.on_message(filters.command('del',prefixes=prefix) & filters.me)
async def delete_com(_,msg: types.Message):
    if msg.from_user.is_self==True:
        await app.delete_messages(msg.chat.id,msg.reply_to_message_id)
        await msg.delete()
    elif msg.from_user.is_self==False:
        await warn(app,msg,'Это не ваше сообщение.',False)
        
@app.on_message(filters.command('getmsg',prefixes=prefix) & filters.me)
async def getmsg_com(_,msg: types.Message):
    print(msg)
    await warn(app,msg,'Данные выведены в консоль.',False,mode='info')

@app.on_message(filters.command('online',prefixes=prefix) & filters.me)
async def online_com(_,msg: types.Message):
    global stoponline
    await warn(app,msg,'Always Online',mode='info')
    while True:
        if stoponline==False:
            online = await app.send_message('me','.')
            await app.delete_messages('me', online.id)
            await asyncio.sleep(10)
        elif stoponline==True:
            stoponline=False
            break
@app.on_message(filters.command('offline',prefixes=prefix) & filters.me)
async def offline_com(_,msg: types.Message):
    global stoponline
    await warn(app,msg,'Постоянный онлайн выключен.',mode='info')
    stoponline=True

@app.on_message(filters.command('action',prefixes=prefix) & filters.me)
async def action_com(_,msg: types.Message):
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

@app.on_message(filters.command('loveword',prefixes=prefix) & filters.me)#idea by my gf, zen1tliks
async def love_com(_,msg: types.Message):
    try:gender = str(msg.text).split(' ')[1]
    except IndexError:await warn(app,msg,'Выберите пол, [m,w]!');return None
    else:
        if not gender in ['m','w']:
            await warn(app,msg,'Выберите пол, [m,w]!');return None
        else:
            if gender == 'm':
                await msg.edit(bold(str(random.choice(love_words)).capitalize())+' ❤️')
            elif gender == 'w':
                await warn(app,msg,'Пока-что нету!')

@app.on_message(filters.command('update',prefixes=prefix) & filters.me)
async def update_com(_,msg: types.Message):
    await msg.edit(bold('🕔 Обновляюсь...'))
    check_version(True)
    await warn(app,msg,'✅ Обновление прошло успешно, напишите .restart для перезагрузки.',mode='info')

@app.on_message(filters.command('restart',prefixes=prefix) & filters.me)
async def restart_com(_,msg: types.Message):
    await warn(app,msg,'Перезагружаюсь, подождите пару секунд...',mode='info')

    restart()

@app.on_message(filters.command('ню',prefixes=prefix) & filters.me)
async def ny_com(_,msg: types.Message):
    try:
        await app.delete_messages(msg.chat.id,msg.id)
        await app.forward_messages('me',msg.chat.id,msg.reply_to_message.id)
    except AttributeError:
        await app.delete_messages(msg.chat.id,msg.id)

@app.on_message(filters.command('quit',prefixes=prefix) & filters.me)
async def quit_com(_,msg: types.Message):
    await warn(app,msg,'Выключаюсь...',mode='info')

    quit()

#On messages
@app.on_message(filters.all | filters.me | filters.private)
async def write_self(_,msg: types.Message):
    if msg.from_user!=None:
        global htext,hideset,tts
        if msg.from_user.is_self == True:
            if str(htext.getstatus()).lower()=='t':
                msg2 = msg;msg2.text = '.type '+msg.text;await type_com(_,msg2)
            elif str(hideset.getstatus()).lower()=='t':
                await msg.edit('||'+msg.text[4:]+'||')
            elif str(ttsset.getstatus()).lower()=='t':
                if msg.text!=None:
                    msg2 = msg;msg2.text = '.tts ru '+msg.text;await tts_com(_,msg2)
            elif str(skullset.getstatus()).lower()=='t':
                if msg.text!=None:
                    await msg.edit(msg.text+' 💀')
            elif str(terminalset.getstatus()).lower()=='t':
                if msg.text!=None:
                    msg2 = msg;msg2.text = '.popen '+msg.text;await popen_com(_,msg)
            elif str(nospaceset.getstatus()).lower()=='t':
                if msg.text!=None:
                    try:
                        await msg.edit(str(msg.text).replace(' ',''))
                    except errors.exceptions.bad_request_400.MessageNotModified:
                        pass

        elif msg.from_user.is_self == False:
            if str(autoreac.getstatus()).lower()=='t':
                await app.send_reaction(msg.chat.id, msg.id, random.choice(['🔥','👍']))      

def run():#Run userbot
    print(getlogo(),end='')
    print(f'''
By: https://t.me/PLNT_YT with ❤️
Your system is: {str(platform.system())}
Started at: {getUptime()} ⏳
Glory to Ukraine!''')
    try:

        app.run()

    except sqlite3.OperationalError:
        #if str(platform.system()).lower() == 'linux':
        #    print('\n\nYou have sqlite3 error!\nEnter: "fuser my_account.session"\nAnd check number at end\nAnd type: "kill -9 <number in command fuser>"\n\n')
        #elif str(platform.system()).lower() == 'windows':
        #    print('\n\nYou have sqlite3 error!\nOpen cmd and enter: taskkill /F /IM python.exe\n\n')

        print("\nYou have sqlite3 error! Don't be worry, we fix that")

        for proc in psutil.process_iter():
            if proc.name().startswith('python'):
                currect_pid = os.getpid()
                if proc.pid != currect_pid:
                    print(f'Found another python instance with pid: {str(proc.pid)}, kill it!')
                    proc.kill()

        print('Restart userbot to fix sqlite3 error!')
        restart()
        
run()