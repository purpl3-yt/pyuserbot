from pyrogram import *
from pyrogram.errors import FloodWait
from download import download
from asyncio import sleep
from PIL import ImageDraw,ImageFont,Image
import io
import os,shutil
import configparser
import requests
import math, random
import string
import socket
import struct
stop=False
config = configparser.ConfigParser()
config.read(r'./settings.ini')
def changestop(newstop):
    global stop
    stop = newstop

def update():
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
def getlogo():
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
#For msgs
async def warn(app,msg,warn: str,alt = False,delay = 3):
    if alt==False:
        await msg.edit('<code>'+str(warn)+'</code>')
        await sleep(delay)
        await msg.delete()
    elif alt==False:
        warn_msg = await app.send_msg(msg.chat.id,'<code>'+str(warn)+'</code>')
        await sleep(delay)
        await warn_msg.delete()
async def getprofile(msg):
    with open('version.txt') as f:
        version = f.read()
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
    
async def jac_img(app,msg,setting=False):
    ufr = requests.get('https://github.com/Sad0ff/modules-ftg/raw/master/open-sans.ttf')
    f = ufr.content
    pic = requests.get('https://www.meme-arsenal.com/memes/54c7ee322f4b0ae586ec96195a59a073.jpg')
    pic.raw.decode_content = True
    img = Image.open(io.BytesIO(pic.content)).convert('RGB')

    W, H = img.size
    #txt = txt.replace('\n', '𓃐')
    if setting==False:
        if msg.reply_to_message!=None:
            text = '\n'.join(str(msg.reply_to_message.text).split(' ')[0:])
            t = text + '\n'
        else:
            text = '\n'.join(str(msg.text).split(' ')[1:])
            t = text + '\n'
    else:
        text = '\n'.join(str(msg.text).split(' ')[0:])
        t = text + '\n'
    await msg.delete()
    #t = t.replace('𓃐','\n')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(io.BytesIO(f), 32, encoding='UTF-8')
    w, h = draw.multiline_textsize(t, font=font)
    imtext = Image.new('RGBA', (w+10, h+10), (0, 0,0,0))
    draw = ImageDraw.Draw(imtext)
    draw.multiline_text((10, 10),t,(0,0,0),font=font, align='left')
    imtext.thumbnail((339, 181))
    w, h = 339, 181
    img.paste(imtext, (10,10), imtext)
    out = io.BytesIO()
    out.name = 'shak.jpg'
    img.save(out)
    out.seek(0)
    await app.send_photo(msg.chat.id,out)
umemes = ['uno','like','salt','vojac','femboy']
async def meme(app: Client,msg,meme):
    if meme == 'uno':#карточки реверса
        uno_cards_urls = ['CAACAgQAAxkBAAL2wWNZDQ9KquGC7PDmBeJz8zNUIZFAAAIFAAPVcf0xIvIu5opGXfMeBA','CAACAgQAAxkBAAL2w2NZDWTAis0LomAb4mndQmK5ZXb5AAIEAAPVcf0xXSRFIA9A-v4eBA','CAACAgQAAxkBAAL2xGNZDWSiIjvV-G3ItXZBB4TvBUzZAAIDAAPVcf0xtgnebiE3rAEeBA','CAACAgQAAxkBAAL2xWNZDWQuQdQsB3PkdZCsLb3hqHanAAICAAPVcf0x1qyFAAFPPAsOHgQ']
        random_card = random.choice(uno_cards_urls)
        await app.send_sticker(msg.chat.id, random_card)
        await msg.delete()
    
    elif meme == 'like':#лайк
        likes_urls = ['CAACAgIAAxkBAAL2_WNZDrV6Zgc4pmMJTdoJC-8gPXEdAAKPGAACh-4hSbfyhIqPrJeUHgQ','CAACAgIAAxkBAAL2_mNZDrvyu-25Jm3VDERwXQthLuyRAAI0AAOROZwcpUsVS-iiqS8eBA']
        random_like = random.choice(likes_urls)
        await app.send_sticker(msg.chat.id,random_like)
        await msg.delete()
    
    elif meme == 'salt':#соль
        await msg.delete()
        await app.send_sticker(msg.chat.id,'CAACAgIAAxkBAAL3S2NZEhHTWI96BhcvSvVB48TB9jvfAAIOGAACaJzQS2XR7x4eNashHgQ')
    
    elif meme == 'vojak':
        vojac_urls = ['CAACAgQAAxkBAAL3T2NZEiOODzyS00sTBJA1gidAwt_eAAIFAQAC5JMqMIzUKlEXfKTPHgQ','CAACAgQAAxkBAAL3TGNZEhd-fYe2PuXs0ySabFhtxrNtAAIEAQAC5JMqMBtErOcuQV9AHgQ']
        random_vojak = random.choice(vojac_urls)
        await app.send_sticker(msg.chat.id,random_vojak)
        await msg.delete()
    
    elif meme == 'femboy':
        await app.send_sticker(msg.chat.id,'CAACAgIAAxkDAAEBnv1jk3S0p1-Gb8eeCdI66kmqyhps8AACHyIAAj3TiUjy-U0IEBjqWR4E')
    
    #Removed not working memes