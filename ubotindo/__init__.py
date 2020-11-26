# UserindoBot
# Copyright (C) 2020  UserindoBot Team, <https://github.com/MoveAngel/UserIndoBot.git>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
import sys
import spamwatch
from telethon import TelegramClient
import telegram.ext as tg

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)
aps_logger = logging.getLogger('apscheduler')
aps_logger.setLevel(logging.WARNING)    

LOGGER = logging.getLogger(__name__)
LOGGER.info("Starting ubotindo...")

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    sys.exit(1)

# Check if system is reboot or not
try:
    os.remove("reboot")
except BaseException:
    pass

ENV = bool(os.environ.get("ENV", False))

if ENV:
    TOKEN = os.environ.get("TOKEN", None)
    try:
        OWNER_ID = int(os.environ.get("OWNER_ID", None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    MESSAGE_DUMP = os.environ.get("MESSAGE_DUMP", None)
    GBAN_LOGS = os.environ.get("GBAN_LOGS", None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

    try:
        DEV_USERS = set(
            int(x) for x in os.environ.get(
                "DEV_USERS", "").split())
    except ValueError:
        raise Exception("Your dev users list does not contain valid integers.")

    try:
        SUDO_USERS = set(
            int(x) for x in os.environ.get(
                "SUDO_USERS", "").split())
    except ValueError:
        raise Exception(
            "Your sudo users list does not contain valid integers.")

    try:
        SUPPORT_USERS = set(
            int(x) for x in os.environ.get(
                "SUPPORT_USERS", "").split())
    except ValueError:
        raise Exception(
            "Your support users list does not contain valid integers.")

    try:
        WHITELIST_USERS = set(
            int(x) for x in os.environ.get("WHITELIST_USERS", "").split()
        )
    except ValueError:
        raise Exception(
            "Your whitelisted users list does not contain valid integers.")
    try:
        WHITELIST_CHATS = set(
            int(x) for x in os.environ.get("WHITELIST_CHATS", "").split()
        )
    except ValueError:
        raise Exception(
            "Your whitelisted users list does not contain valid integers.")
    try:
        BLACKLIST_CHATS = set(
            int(x) for x in os.environ.get("BLACKLIST_CHATS", "").split()
        )
    except ValueError:
        raise Exception(
            "Your whitelisted users list does not contain valid integers.")

    WEBHOOK = bool(os.environ.get("WEBHOOK", False))
    URL = os.environ.get("URL", "")  # Does not contain token
    PORT = int(os.environ.get("PORT", 5000))
    CERT_PATH = os.environ.get("CERT_PATH")

    DB_URI = os.environ.get("DATABASE_URL")
    DONATION_LINK = os.environ.get("DONATION_LINK")
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "").split()
    DEL_CMDS = bool(os.environ.get("DEL_CMDS", False))
    STRICT_GBAN = bool(os.environ.get("STRICT_GBAN", False))
    WORKERS = int(os.environ.get("WORKERS", 8))
    BAN_STICKER = os.environ.get(
        "BAN_STICKER",
        "CAADAgADOwADPPEcAXkko5EB3YGYAg")
    CUSTOM_CMD = os.environ.get("CUSTOM_CMD", False)
    API_WEATHER = os.environ.get("API_OPENWEATHER", None)
    WALL_API = os.environ.get("WALL_API", None)
    TELETHON_ID = int(os.environ.get("TL_APP_ID", None))
    TELETHON_HASH = os.environ.get("TL_HASH", None)
    SPAMWATCH = os.environ.get("SPAMWATCH_API", None)

else:
    from ubotindo.config import Development as Config

    TOKEN = Config.API_KEY
    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")

    OWNER_USERNAME = Config.OWNER_USERNAME
    MESSAGE_DUMP = Config.MESSAGE_DUMP
    GBAN_LOGS = Config.GBAN_LOGS

    try:
        DEV_USERS = set(int(x) for x in Config.DEV_USERS or [])
    except ValueError:
        raise Exception("Your dev users list does not contain valid integers.")

    try:
        SUDO_USERS = set(int(x) for x in Config.SUDO_USERS or [])
    except ValueError:
        raise Exception(
            "Your sudo users list does not contain valid integers.")

    try:
        SUPPORT_USERS = set(int(x) for x in Config.SUPPORT_USERS or [])
    except ValueError:
        raise Exception(
            "Your support users list does not contain valid integers.")

    try:
        WHITELIST_USERS = set(int(x) for x in Config.WHITELIST_USERS or [])
    except ValueError:
        raise Exception(
            "Your whitelisted users list does not contain valid integers.")
    try:
        WHITELIST_CHATS = set(int(x) for x in Config.WHITELIST_CHATS or [])
    except ValueError:
        raise Exception(
            "Your whitelisted users list does not contain valid integers.")
    try:
        BLACKLIST_CHATS = set(int(x) for x in Config.BLACKLIST_CHATS or [])
    except ValueError:
        raise Exception(
            "Your whitelisted users list does not contain valid integers.")

    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH

    DB_URI = Config.SQLALCHEMY_DATABASE_URI
    DONATION_LINK = Config.DONATION_LINK
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    DEL_CMDS = Config.DEL_CMDS
    STRICT_GBAN = Config.STRICT_GBAN
    WORKERS = Config.WORKERS
    BAN_STICKER = Config.BAN_STICKER
    # ALLOW_EXCL = Config.ALLOW_EXCL
    CUSTOM_CMD = Config.CUSTOM_CMD
    API_WEATHER = Config.API_OPENWEATHER
    WALL_API = Config.WALL_API
    TELETHON_HASH = Config.TELETHON_HASH
    TELETHON_ID = Config.TELETHON_ID
    SPAMWATCH = Config.SPAMWATCH_API

DEV_USERS.add(OWNER_ID)

# Pass if SpamWatch token not set.
if SPAMWATCH is None:
    spamwtc = None
    LOGGER.warning("Invalid spamwatch api")
else:
    spamwtc = spamwatch.Client(SPAMWATCH)

# Telethon
api_id = TELETHON_ID
api_hash = TELETHON_HASH
client = TelegramClient("ubotindo", api_id, api_hash)

updater = tg.Updater(TOKEN, workers=WORKERS)

dispatcher = updater.dispatcher

# Declare user rank
DEV_USERS = list(DEV_USERS)
SUDO_USERS = list(SUDO_USERS)
SUPPORT_USERS = list(SUPPORT_USERS)

STAFF = DEV_USERS + SUDO_USERS + SUPPORT_USERS
STAFF_USERS = list(STAFF)

WHITELIST_USERS = list(WHITELIST_USERS)

# Load at end to ensure all prev variables have been set
from ubotindo.modules.helper_funcs.handlers import CustomCommandHandler  # noqa: disable wrong import module

if CUSTOM_CMD and len(CUSTOM_CMD) >= 1:
    tg.CommandHandler = CustomCommandHandler
