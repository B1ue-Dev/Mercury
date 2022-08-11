"""
Bot's constant.

(C) 2022 - Jimmy-Blue
"""

import os
import dotenv
dotenv.load_dotenv()

global TOKEN
global MODMAIL_CHANNEL
global SCOPE
global EXTENSION

TOKEN = os.getenv('TOKEN')
MODMAIL_CHANNEL = os.getenv('MODMAIL_CHANNEL')
SCOPE = int(os.getenv('SCOPE'))
EXTENSION = [file.replace(".py", "") for file in os.listdir("exts") if not file.startswith("_")]
