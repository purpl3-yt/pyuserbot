from utils import check_version
from userbot import run

try:
    from download import download
    from gtts import gTTS
    import pyrogram
    import requests
except ImportError:
    import os,shutil
    print('Wait, we install libraries')
    os.system('pip install -r imports.txt')


check_version()

run()#Run userbot