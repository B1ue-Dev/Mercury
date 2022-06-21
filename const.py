"""
Bot's constant.

(C) 2022 - Jimmy-Blue
"""

import os
import dotenv
dotenv.load_dotenv()

TOKEN = os.getenv('TOKEN')
MODMAIL_CHANNEL = os.getenv('MODMAIL_CHANNEL')
SCOPE = os.getenv('SCOPE')