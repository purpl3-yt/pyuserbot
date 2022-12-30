from pyrogram.errors import FloodWait
from download import download
from os import execl, path
from asyncio import sleep
from pyrogram import *
import os,shutil,sys
import math, random
import configparser
import requests
import string
import socket
import struct
import time
stop=False
config = configparser.ConfigParser()
config.read(r'./settings.ini')
def changestop(newstop):
    global stop
    stop = newstop

def update():#bad update system :(
    files = ['userbot.py','version.txt','utils.py','main.py']
    if not os.path.isdir('./newfiles'):
        os.mkdir('./newfiles')
    for i in files:
        newfiles = download(
            url=f'https://raw.githubusercontent.com/purpl3-yt/pyuserbot/master/{i}',path='./newfiles',replace=True,progressbar=True
        )
        os.remove(f'./{i}')
        shutil.move('./newfiles/newfiles.part','./')
        os.rename('./newfiles.part',f'./{i}')

def check_version(force=False):
    if not force:
        newversion = requests.get('https://raw.githubusercontent.com/purpl3-yt/pyuserbot/master/version.txt')
        with open('version.txt') as f:
            oldversion = f.read()
            f.close()
        if oldversion == newversion.text:
            print('Userbot is up to date')
        elif oldversion != newversion.text:
            update()
    elif force:
        update()

def check_run():
    times = 0

    while True:
        time.sleep(2)
        print(1)
        if times>=5:
            return False 
        
        if os.path.isfile('./my_account.session-journal'):
            return True


def text_animation(text):
    symbols = ['*','@','#','$','%','^','&','&']
    temp = text
    temp+=temp[:1]
    shif = []
    for i in range(1,len(temp)+1):
        shif.append(random.choice(symbols))
    steps = []
    phrase = []
    for i in range(1,int(len(temp))+1):
        phrase.append(temp[i-1:i])
    x = 0
    for i in phrase:
        shif.pop(x)
        str = ''.join(shif)
        steps.append(str)
        shif.insert(x,i)
        str = ''.join(shif)
        x+=1
    return steps

def generatehackerstr(lenght):
    symbols = ['!','@','#','$','%','^','&','*','(',')','{','}','[',']']
    hackerstr = ''
    for i in range(0,int(lenght)):
        hackerstr+=random.choice(symbols)
    return hackerstr

def getrandomgeo():
    pi = math.pi
    cf = 180.0 / pi 

    gx = random.gauss(0.0, 1.0)
    gy = random.gauss(0.0, 1.0)
    gz = random.gauss(0.0, 1.0)

    norm2 = gx*gx + gy*gy + gz*gz
    norm1 = 1.0 / math.sqrt(norm2)
    x = gx * norm1
    y = gy * norm1
    z = gz * norm1

    radLat = math.asin(z)   
    radLon = math.atan2(y,x)
    return (round(cf*radLat, 5), round(cf*radLon, 5))

def getrandomip():
    return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

def getrandomhwid():
    random_ascii = string.ascii_uppercase
    random_digits = string.digits
    hwid = ''
    for i in range(0,random.randint(18,23)):
        hwid+=random.choice(random_ascii)
        hwid+=random.choice(random_digits)
    return hwid

def str_to_class(classname):#return class
    return getattr(sys.modules[__name__], classname)

def getlogo():
    header = '''
  _____       _    _               ____        _   
 |  __ \     | |  | |             |  _ \      | |  
 | |__) |   _| |  | |___  ___ _ __| |_) | ___ | |_ 
 |  ___/ | | | |  | / __|/ _ \ '__|  _ < / _ \| __|
 | |   | |_| | |__| \__ \  __/ |  | |_) | (_) | |_ 
 |_|    \__, |\____/|___/\___|_|  |____/ \___/ \__|
         __/ |                                     
        |___/                                      
'''
    return header

#Classes
class Setting:
    def __init__(self,name,status):
        self.name = name
        self.status = status
    def getname(self):
        return self.name
    def getstatus(self):
        return self.status
    def setstatus(self,newstatus):
        self.status = newstatus

memes = []

class Meme:
    def __init__(self,name,category,url):
        self.name = name
        self.category = category
        self.url = url
        memes.append(self)

    async def send(self,app,msg):
        if type(self.url) == str and str(self.url).startswith('CAAC'):
            await app.send_sticker(msg.chat.id,self.url)
        if type(self) == str and not str(self.url).startswith('CAAC'):
            await app.send_message(msg.chat.id,self.url)
        if type(self.url) == list:
            await app.send_sticker(msg.chat.id,random.choice(self.url))
    
    def getname(self):
        return self.name

    def getcategory(self):
        return self.category
#For msgs
async def warn(app,msg,warn: str,alt = False,delay = 3, mode = 'error'):
    if not alt:
        if mode=='error':
            await msg.edit('🚫 '+'<b>'+str(warn)+'</b>')
        elif mode=='info':
            await msg.edit('ℹ️ '+'<b>'+str(warn)+'</b>')
        await sleep(delay)
        await msg.delete()
    elif alt:
        if mode=='error':
            warn_msg = await app.send_message(msg.chat.id,'🚫 '+'<b>'+str(warn)+'</b>')
        elif mode=='info':
            warn_msg = await app.send_message(msg.chat.id,'ℹ️ '+'<b>'+str(warn)+'</b>')
        await sleep(delay)
        await warn_msg.delete()

async def getprofile(msg):
    with open('version.txt') as f:
        version = f.read()

    convert_bool = {True:'Да',False:'Нет'}

    git_ver = requests.get('https://raw.githubusercontent.com/purpl3-yt/pyuserbot/master/version.txt')
    github_version = git_ver.text
    if msg.reply_to_message==None:
        name = msg.from_user.username
        is_premium = convert_bool[msg.from_user.is_premium]
        is_scam = convert_bool[msg.from_user.is_scam]
        is_bot = convert_bool[msg.from_user.is_bot]
        await msg.edit(f'''
✏️ Имя: <b>{name}</b>
⭐️ С премиумом: {is_premium}</b>
🥸 Скам: <b>{is_scam}</b>
🤖 Бот: <b>{is_bot}</b>
🗒 Версия юзер бота: <code>{version}</code>
🗒 Версия юзер бота на гитхаб: <code>{github_version}</code>
🌐 <a href='https://github.com/purpl3-yt/pyuserbot'>Репозиторий</a>''',disable_web_page_preview=True)

    else:
        first_name = msg.reply_to_message.from_user.first_name
        last_name = msg.reply_to_message.from_user.last_name
        name = msg.reply_to_message.from_user.username
        is_premium = convert_bool[msg.reply_to_message.from_user.is_premium]
        is_scam = convert_bool[msg.reply_to_message.from_user.is_scam]
        is_bot = convert_bool[msg.reply_to_message.from_user.is_bot]
        await msg.edit(f'''
✏️ Первое имя: <b>{first_name}</b>
✏️ Второе имя: <b>{last_name}</b>
#️⃣ Тег: @{name}
⭐️ С премиумом: <b>{is_premium}</b>
🥸 Скам: <b>{is_scam}</b>
🤖 Бот: <b>{is_bot}</b>''')

async def disappear(msg,str: str,step: int):#For anim
    steps = []
    for i in range(0,len(str)+1,step):
        steps.append(str[:i])
    steps.pop(int(len(steps)-1))
    for i in steps[::-1]:
        if i=='':
            break
        await msg.edit(i)
        await sleep(0.1)
    await msg.delete()

async def count_anim(msg):
    global stop
    gh = 1000
    gh_list = []
    for i in range(0,gh+1):
        if str(i-1)[:1]=='-':
            continue
        gh_list.append(f'{str(i)} - 1 = {str(i-1)}')
    gh_list.reverse()
    for i in gh_list:
        if stop==True:
            await msg.delete()
            stop=False   
            break
        try:
            await msg.edit(i)
        except FloodWait as wait:
            await sleep(wait)
        await sleep(0.1)

async def usky(msg):
    global stop
    squares = ['🟥','🟧','🟨','🟩','🟦','🟪']
    def generateline():
        anim = []
        for i in range(0,17):
            anim.append(random.choice(squares))
        return anim
    for i in range(0,9):#symbols lenght
        if stop==True:
            await msg.delete()
            stop=False   
            break
        sky = ''.join(generateline())*6+'\n'
        try:
            await msg.edit(sky)
        except FloodWait as wait:
            await sleep(wait)
        await sleep(0.2)
    await disappear(msg,sky,4)
    
async def umath(msg,num1,oper,num2,app=None):
    try:
        if oper=='+':await msg.edit(int(num1)+int(num2))
        elif oper=='-':await msg.edit(int(num1)-int(num2))
        elif oper=='/':await msg.edit(int(num1)/int(num2))
        elif oper=='*':await msg.edit(int(num1)*int(num2))
    except ValueError:
        await warn(app,msg,'Введите числа а не буквы!')

#Memes
meme_uno = Meme('Uno','Games',['CAACAgQAAxkBAAL2wWNZDQ9KquGC7PDmBeJz8zNUIZFAAAIFAAPVcf0xIvIu5opGXfMeBA','CAACAgQAAxkBAAL2w2NZDWTAis0LomAb4mndQmK5ZXb5AAIEAAPVcf0xXSRFIA9A-v4eBA','CAACAgQAAxkBAAL2xGNZDWSiIjvV-G3ItXZBB4TvBUzZAAIDAAPVcf0xtgnebiE3rAEeBA','CAACAgQAAxkBAAL2xWNZDWQuQdQsB3PkdZCsLb3hqHanAAICAAPVcf0x1qyFAAFPPAsOHgQ'])
meme_like = Meme('Like','Emote',['CAACAgIAAxkBAAL2_WNZDrV6Zgc4pmMJTdoJC-8gPXEdAAKPGAACh-4hSbfyhIqPrJeUHgQ','CAACAgIAAxkBAAL2_mNZDrvyu-25Jm3VDERwXQthLuyRAAI0AAOROZwcpUsVS-iiqS8eBA'])
meme_vojac = Meme('Vojac','Emote',['CAACAgQAAxkBAAL3T2NZEiOODzyS00sTBJA1gidAwt_eAAIFAQAC5JMqMIzUKlEXfKTPHgQ','CAACAgQAAxkBAAL3TGNZEhd-fYe2PuXs0ySabFhtxrNtAAIEAQAC5JMqMBtErOcuQV9AHgQ'])
meme_salt = Meme('Salt','Item','CAACAgIAAxkBAAL3S2NZEhHTWI96BhcvSvVB48TB9jvfAAIOGAACaJzQS2XR7x4eNashHgQ')
meme_femboy = Meme('Femboy','Cringe','CAACAgIAAxkDAAEBnv1jk3S0p1-Gb8eeCdI66kmqyhps8AACHyIAAj3TiUjy-U0IEBjqWR4E')
meme_femkiss = Meme('Femkiss','Cringe','CAACAgIAAxkDAAEByFNjmD0WQfCltUPXMJojwhfH9qCzfwACkyEAAmWJiUhQ5-ExHW4vWR4E')
meme_oleg = Meme('Oleg','Emote','CAACAgIAAx0CZwXFtAABAbNtY5SIosrOCxj9HQIoidO27ydBZocAAhEVAAJLhgABSJ6bJubgLqHXHgQ')
meme_bruh = Meme('Bruh','Emote','CAACAgIAAx0EcPHO9gACDrhjlvgc2L9WeDjEJwYTdC9IDDRMDgACaxUAAvhCAAFI6ZIBkR_3m9QeBA')
meme_hard = Meme('Hard','Item','CAACAgIAAxkBAAEByWZjmFO67mnzSGdrQpksKgHMcCOl5wAC6xgAAnCIoUk9DxK770v4jx4E')
meme_drink = Meme('Drink','Item','CAACAgIAAxkDAAEB5QxjnYjat9Bc2P64Sh5CkKI2wes23wACExcAAsISAAFIimUEhOYchxoeBA')
meme_idk = Meme('Idk','Emote','CAACAgIAAxkDAAEB_lxjoB4s8JnjrONFiaelO3e-qzRHDgACmwADkTmcHJTkgPOvMYNPHgQ')
meme_cool = Meme('Cool','Emote','CAACAgIAAxkBAAEB_m5joB6XSUpy0zL3xiXGnyQPF4DhPgACPg8AAn9puUvb6DZzd3HGxR4E')
meme_sus = Meme('Sus','Emote','CAACAgIAAxkBAAEB_nBjoB67rlYHCZTHQQNWffUOe4qVUQACJCAAAv-n-Eg1mD0n5qr6Nh4E')
meme_gigachad = Meme('Gigachad','Emote','CAACAgQAAxkBAAEB_nJjoB7aQWNRtz-3d1gZGWZT7DycZQACEgMAAqHa1A9Qu6d81h2qdB4E')
meme_dance = Meme('Dance','Emote','CAACAgIAAxkBAAECbZBjqZ0qUsILfOUfTFa25X5xdMftLgAC1hQAAm-4-UucNlgIIZ1nrh4E')
meme_dance2 = Meme('Dance2','Emote','CAACAgIAAxkDAAECbsNjqaHvkCMetrk8cREpEnIpXSzDgwACSBYAApxiAUhjyjg_YD5u5R4E')
meme_tractor = Meme('Tractor','Item','CAACAgIAAxkDAAECn1tjq2uDVBgqQ18YptfXu22qf6i_OAACkxMAAkRtCEnpNJHfOGwvTx4E')
meme_say = Meme('Say','Emote','CAACAgIAAxkDAAECn1pjq2uYVLVivetbuhSBo10-CGivWwACLxIAAhg_0UtM8KolgQ4LWB4E')
meme_wow = Meme('Wow','Emote','CAACAgIAAxkDAAECoM1jq3UWPPAl9TKeXdyzfnhJj1V0ZgACdRUAAneE2EtBa1RDx5PwIR4E')
meme_artem = Meme('Artem','Item','CAACAgIAAxkDAAECsuRjrhLFr79OuEc_aR3kNyMQ2c4LEQACKR0AAhoNCUnTlkTj29nSVB4E')

umemes = {}
for mem in memes:
    try:
        umemes[str(mem.getcategory()).lower()]
    except KeyError:
        umemes[str(mem.getcategory()).lower()] = []    

for mem in memes:
    umemes[str(mem.getcategory()).lower()].append(mem)
