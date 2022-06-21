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

TOKEN = os.getenv('TOKEN')
MODMAIL_CHANNEL = os.getenv('MODMAIL_CHANNEL')
SCOPE = int(os.getenv('SCOPE'))
