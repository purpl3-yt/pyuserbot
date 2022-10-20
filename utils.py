from pyrogram import *
from pyrogram.errors import FloodWait
stop=False

def changestop(newstop):
    global stop
    stop = newstop

def update():
    import os,shutil
    from download import download
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
    import requests
    if force==False:
        newversion = requests.get('https://raw.githubusercontent.com/purpl3-yt/pyuserbot/master/version.txt')
        with open('version.txt') as f:
            oldversion = f.read()
            f.close()
        if oldversion == newversion.text:
            print('Userbot is up to date')
        elif oldversion != newversion.text:
            update()
    elif force==True:
        update()

def text_animation(text):
    from random import choice
    symbols = ['!','@','#','$','%','^','&','*','(',')','{','}','[',']']
    temp = text
    temp+=temp[:1]
    shif = []
    for i in range(1,len(temp)+1):
        shif.append(choice(symbols))
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
    from random import choice
    symbols = ['!','@','#','$','%','^','&','*','(',')','{','}','[',']']
    hackerstr = ''
    for i in range(0,int(lenght)):
        hackerstr+=choice(symbols)
    return hackerstr

def getrandomgeo():
    import math, random
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
    import random
    import socket
    import struct
    return socket.inet_ntoa(struct.pack(">I", random.randint(1, 0xffffffff)))

def getrandomhwid():
    import string
    import random
    random_ascii = string.ascii_uppercase
    random_digits = string.digits
    hwid = ''
    for i in range(0,random.randint(18,23)):
        hwid+=random.choice(random_ascii)
        hwid+=random.choice(random_digits)
    return hwid
def getlogo():
    from time import sleep
    header = '''
  _    _               ____        _   
 | |  | |             |  _ \      | |  
 | |  | |___  ___ _ __| |_) | ___ | |_ 
 | |  | / __|/ _ \ '__|  _ < / _ \| __|
 | |__| \__ \  __/ |  | |_) | (_) | |_ 
  \____/|___/\___|_|  |____/ \___/ \__|
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

#For messages
async def warn(app,msg,warn: str,alt = False):
    from asyncio import sleep
    if alt==False:
        await msg.edit('<code>'+str(warn)+'</code>')
        await sleep(3)
        await msg.delete()
    elif alt==False:
        warn_msg = await app.send_message(msg.chat.id,'<code>'+str(warn)+'</code>')
        await sleep(3)
        await warn_msg.delete()
async def getprofile(msg):
    with open('version.txt') as f:
        version = f.read()
    import requests
    git_ver = requests.get('https://raw.githubusercontent.com/purpl3-yt/pyuserbot/master/version.txt')
    github_version = git_ver.text
    if msg.reply_to_message==None:
        name = msg.from_user.username
        is_premium = msg.from_user.is_premium
        is_scam = msg.from_user.is_scam
        is_bot = msg.from_user.is_bot
        await msg.edit(f'''
Имя: {name}
Номер телефона: ||куда мы лезем боже||
С премиумом: {is_premium}
Скам: {is_scam}
Бот: {is_bot}
Версия юзер бота: {version}
Версия юзер бота на гитхаб: {github_version}
<a href='https://github.com/purpl3-yt/pyuserbot'>Репозиторий</a>''',disable_web_page_preview=True)

    else:
        first_name = msg.reply_to_message.from_user.first_name
        last_name = msg.reply_to_message.from_user.last_name
        name = msg.reply_to_message.from_user.username
        is_premium = msg.reply_to_message.from_user.is_premium
        is_scam = msg.reply_to_message.from_user.is_scam
        is_bot = msg.reply_to_message.from_user.is_bot
        await msg.edit(f'''
Первое имя: {first_name}
Второе имя: {last_name}
Тег: @{name}
Номер телефона: ||куда мы лезем боже||
С премиумом: {is_premium}
Скам: {is_scam}
Бот: {is_bot}''')
async def disappear(msg,str: str,step: int):#For anim
    from time import sleep
    steps = []
    for i in range(0,len(str)+1,step):
        steps.append(str[:i])
    steps.pop(int(len(steps)-1))
    for i in steps[::-1]:
        if i=='':
            break
        await msg.edit(i)
        sleep(0.1)
    await msg.delete()

async def ghoul_anim(msg):
    global stop
    gh = 1000
    gh_list = []
    for i in range(0,gh+1):
        if str(i-7)[:1]=='-':
            continue
        gh_list.append(f'{str(i)} - 7 = {str(i-7)}')
    gh_list.reverse()
    from time import sleep
    for i in gh_list:
        if stop==True:
            await msg.delete()
            stop=False   
            break
        try:
            await msg.edit(i)
        except FloodWait as wait:
            sleep(wait)
        sleep(0.1)

async def usky(msg):
    global stop
    from random import choice
    from time import sleep
    squares = ['🟥','🟧','🟨','🟩','🟦','🟪']
    def generateline():
        anim = []
        for i in range(0,17):
            anim.append(choice(squares))
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
            sleep(wait)
        sleep(0.2)
    await disappear(msg,sky,4)
    
async def umath(msg,num1,oper,num2,app=None):
    try:
        if oper=='+':await msg.edit(int(num1)+int(num2))
        elif oper=='-':await msg.edit(int(num1)-int(num2))
        elif oper=='/':await msg.edit(int(num1)/int(num2))
        elif oper=='*':await msg.edit(int(num1)*int(num2))
    except ValueError:
        await warn(app,msg,'<code>Введите числа а не буквы</code>')