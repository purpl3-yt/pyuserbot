try:
    import pyrogram
    from download import download
    import requests
    import gtts
except ImportError:
    import os,shutil
    print('Wait, we install libraries')
    if not os.path.isdir('./newfiles'):
        os.mkdir('./newfiles')
    newimports_file = download(
            url='https://raw.githubusercontent.com/purpl3-yt/pyuserbot/master/imports.txt',path='./newfiles',replace=True,progressbar=True
    )
    os.remove('./imports.txt')
    shutil.move('./newfiles/newfiles.part','./')
    os.rename('./newfiles.part','./imports.txt')
    os.system('pip install -r imports.txt')

def update():
    import os,shutil
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
        update
check_version()
from userbot import run
run()#Run userbot