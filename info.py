import re
import os
from os import environ
from pyrogram import enums
from Script import script
from dotenv import load_dotenv

import asyncio
import json
from collections import defaultdict
from typing import Dict, List, Union
from pyrogram import Client

load_dotenv(override=True)

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

class evamaria(Client):
    filterstore: Dict[str, Dict[str, str]] = defaultdict(dict)
    warndatastore: Dict[
        str, Dict[str, Union[str, int, List[str]]]
    ] = defaultdict(dict)
    warnsettingsstore: Dict[str, str] = defaultdict(dict)

    def __init__(self):
        name = self.__class__.__name__.lower()
        super().__init__(
            ":memory:",
            plugins=dict(root=f"{name}/plugins"),
            workdir=TMP_DOWNLOAD_DIRECTORY,
            api_id=APP_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            parse_mode=enums.ParseMode.HTML,
            sleep_threshold=60
        )

# Bot information
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ.get('API_ID', '6620972'))
API_HASH = environ.get('API_HASH', '3f6835286b03e000ab6d71b37cc35b92')
BOT_TOKEN = environ.get('BOT_TOKEN', '6804220356:AAG675PNd7lSY2B8BcAZdpnwenKgR0WDo2o')

# Bot settings
CACHE_TIME = 300
USE_CAPTION_FILTER = False
NOR_IMG = environ.get('NOR_IMG', "https://envs.sh/qhm.jpg")
PICS = (environ.get('PICS', 'https://te.legra.ph/file/f83017d890b1b692a673a.jpg https://te.legra.ph/file/72602fb1f87727dde571b.jpg https://te.legra.ph/file/e37fbea2190470aaf4bc1.jpg https://te.legra.ph/file/9f4f70db519f1bdbcb27b.jpg https://te.legra.ph/file/72d74f632a2317f21136b.jpg https://te.legra.ph/file/018e5893fdaabe0f1cef4.jpg')).split()
SPELL_IMG = environ.get('SPELL_IMG',"https://telegra.ph/file/314928baed9a9c277072f.jpg")

# Welcome area
MELCOW_IMG = environ.get('MELCOW_IMG',"https://telegra.ph/file/4cd231fbe9085ec49e75d.jpg")
MELCOW_VID = environ.get('MELCOW_VID',"https://telegra.ph/file/b26637d70f3630a7e0fa1.mp4")



# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '6874351976 6047510747').split()] 
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1001831375385 -10012345688 -1001658823824 -1001659557643 -1001895564079 -10027378293 -10073837388 -1001765720202').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_grp = environ.get('AUTH_GROUP')
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None
POST_CHANNELS = list(map(int, (channel.strip() for channel in environ.get('POST_CHANNELS', '-1002352843003').split(','))))
# This is required for the plugins involving the file system.
TMP_DOWNLOAD_DIRECTORY = environ.get("TMP_DOWNLOAD_DIRECTORY", "./DOWNLOADS/")

# Command
COMMAND_HAND_LER = ("/")

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://maki:maki@cluster0.5zlhzxl.mongodb.net/?retryWrites=true&w=majority")
DATABASE_URI1 = environ.get('DATABASE_URI1', "mongodb+srv://Maki1:Maki1@cluster0.cafwfcz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_URI2 = environ.get('DATABASE_URI2', "mongodb+srv://Maki2:Maki2@cluster0.jqossy3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_URI3 = environ.get('DATABASE_URI3', "mongodb+srv://Maki3:Maki3@cluster0.lcalwif.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_URI4 = environ.get('DATABASE_URI4', "mongodb+srv://Maki4:Maki4@cluster0.zxpg2fq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_URI5 = environ.get('DATABASE_URI5', "mongodb+srv://Maki5:Maki5@cluster0.gkt7inw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_URI6 = environ.get('DATABASE_URI6', "mongodb+srv://Maki6:Maki6@cluster0.ejxrdei.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DATABASE_NAME = environ.get('DATABASE_NAME', "maki")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'andi')
MONGO_URL = os.environ.get('MONGO_URL', "mongodb+srv://maki:maki@cluster0.2t0eici.mongodb.net/?retryWrites=true&w=majority")

#Downloader
DOWNLOAD_LOCATION = environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS/AudioBoT/")

# Others
DELETE_CHANNELS = [int(dch) if id_pattern.search(dch) else dch for dch in environ.get('DELETE_CHANNELS', '0').split()]
PORT = os.environ.get("PORT", "8680")
MAX_BTN = int(environ.get('MAX_BTN', "10"))
S_GROUP = environ.get('S_GROUP',"https://t.me/CV_linkz")
MAIN_CHANNEL = environ.get('MAIN_CHANNEL',"https://t.me/CV_Official_channel")
FILE_FORWARD = environ.get('FILE_FORWARD',"https://t.me/+TMCviP7KUY8yZjI9")
MSG_ALRT = environ.get('MSG_ALRT', '𝐓𝐡𝐚𝐧𝐤 𝐲𝐨𝐮 𝐒𝐢𝐫 💜')
FILE_CHANNEL = int(environ.get('FILE_CHANNEL', 0))
LOG_CHANNEL =int(environ.get('LOG_CHANNEL', -1002116542152))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'CV_linkZ')
AUTO_DELETE = is_enabled((environ.get('AUTO_DELETE', "False")), False)
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "False")), False)
IMDB = is_enabled((environ.get('IMDB', "True")), True)
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "True")), True)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", f"{script.CUSTOM_FILE_CAPTION}")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", f"{script.IMDB_TEMPLATE_TXT}")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
MAX_LIST_ELM = 4
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "True")), True)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), False)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "False")), False)

#Fsub
# auth_channel = environ.get('AUTH_CHANNEL', "-1002177334603")
# AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
# Set to False inside the bracket if you don't want to use Request Channel else set it to Channel ID
# REQ_CHANNEL =environ.get('REQ_CHANNEL', "-1002177334603")
# REQ_CHANNEL = int(REQ_CHANNEL) if REQ_CHANNEL and id_pattern.search(REQ_CHANNEL) else False
# JOIN_REQS_DB = environ.get("JOIN_REQS_DB", DATABASE_URI)

LOG_STR = "Current Cusomized Configurations are:-\n"
LOG_STR += ("IMDB Results are enabled, Bot will be showing imdb details for you queries.\n" if IMDB else "IMBD Results are disabled.\n")
LOG_STR += ("P_TTI_SHOW_OFF found , Users will be redirected to send /start to Bot PM instead of sending file file directly\n" if P_TTI_SHOW_OFF else "P_TTI_SHOW_OFF is disabled files will be send in PM, instead of sending start.\n")
LOG_STR += ("SINGLE_BUTTON is Found, filename and files size will be shown in a single button instead of two separate buttons\n" if SINGLE_BUTTON else "SINGLE_BUTTON is disabled , filename and file_sixe will be shown as different buttons\n")
LOG_STR += (f"CUSTOM_FILE_CAPTION enabled with value {CUSTOM_FILE_CAPTION}, your files will be send along with this customized caption.\n" if CUSTOM_FILE_CAPTION else "No CUSTOM_FILE_CAPTION Found, Default captions of file will be used.\n")
LOG_STR += ("Long IMDB storyline enabled." if LONG_IMDB_DESCRIPTION else "LONG_IMDB_DESCRIPTION is disabled , Plot will be shorter.\n")
LOG_STR += ("Spell Check Mode Is Enabled, bot will be suggesting related movies if movie not found\n" if SPELL_CHECK_REPLY else "SPELL_CHECK_REPLY Mode disabled\n")
LOG_STR += (f"MAX_LIST_ELM Found, long list will be shortened to first {MAX_LIST_ELM} elements\n" if MAX_LIST_ELM else "Full List of casts and crew will be shown in imdb template, restrict them by adding a value to MAX_LIST_ELM\n")
LOG_STR += f"Your current IMDB template is {IMDB_TEMPLATE}"
