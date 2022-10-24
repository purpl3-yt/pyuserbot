try:
    import pyrogram
    from download import download
    import requests
    from gtts import gTTS
    import pathlib
except ImportError:
    import os,shutil
    from download import download
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

from utils import check_version
check_version()
from userbot import run
run()#Run userbot