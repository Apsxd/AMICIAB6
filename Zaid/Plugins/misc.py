import asyncio
import json
import os
import random
import re
from datetime import datetime

from bing_image_urls import bing_image_urls
from bs4 import BeautifulSoup
from geniuses import GeniusClient
from gpytranslate import SyncTranslator
from gtts import gTTS
from mutagen.mp3 import MP3
from PIL import Image
from requests import get, post
from telethon import Button, types
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    Channel,
    DocumentAttributeAudio,
    MessageMediaDocument,
    PhotoEmpty,
    User,
)

from config import BOT_ID, OWNER_ID
from Zaid import Zaid, CMD_HELP
from ..utils import Zbot, Zinline
from . import DEVS, SUDO_USERS, db, get_user, human_format
from .mongodb.couples_db import (
    add_vote_down,
    add_vote_up,
    get_couple,
    rm_vote_down,
    rm_vote_up,
    save_couple,
    voted_down,
    voted_up,
)
from .language import translate

gbanned = db.gbanned
user_about_x = db.about_users

AZURE_API_KEY_URL_PREVIEW = "27b02a2c7d394388a719e0fdad6edb10"


@Zbot(pattern="^/id ?(.*)")
async def aa(event):
    if not event.reply_to and not event.pattern_match.group(1):
        str(event.chat_id).replace("-100", "")
        return await event.reply(translate(f"This chat's ID is: `{event.chat_id}`", event.chat_id))
    user = None
    try:
        user, extra = await get_user(event)
        user_id = user.id
        name = user.first_name
        if not name:
            name = "User"
    except:
        pass
    if event.reply_to:
        msg = await event.get_reply_message()
        if msg.fwd_from:
            if msg.fwd_from.saved_from_peer:
                if isinstance(msg.fwd_from.saved_from_peer, types.PeerChannel):
                    try:
                        f_ch = await event.client.get_entity(
                            msg.fwd_from.saved_from_peer.channel_id
                        )
                    except:
                        return
                    skel_channel_post = translate(f"The posted channel, {f_ch.title}, has an id of `-100{f_ch.id}`.", event.chat_id)
                    return await event.reply(skel_channel_post)
            elif msg.fwd_from.from_id:
                if isinstance(msg.fwd_from.from_id, types.PeerUser):
                    try:
                        f_user = await event.client.get_entity(msg.fwd_from.from_id)
                    except:
                        return
                    return await event.reply(translate(f"User {name}'s ID is `{user_id}`.The forwarded user, {f_user.first_name}, has an ID of `{f_user.id}`", event.chat_id))
                elif isinstance(msg.fwd_from.from_id, types.PeerChannel):
                    try:
                        f_chat = await event.client.get_entity(msg.fwd_from.from_id)
                    except:
                        return
                    return await event.reply(translate(f"User {name}'s ID is `{user_id}`.The forwarded channel, {f_chat.title}, has an id of `-100{f_chat.id}`.", event.chat_id))
    await event.reply(translate(f"User {name}'s ID is `{user_id}`.", event.chat_id))



@Zbot(pattern="^/info ?(.*)")
async def _info(e):
    event = e
    if not e.reply_to and not e.pattern_match.group(1):
        if e.sender_id:
            x_user = e.sender
    elif e.reply_to:
        reply_msg = await e.get_reply_message()
        if not reply_msg.sender_id:
            return
        x_user = reply_msg.sender
    elif e.pattern_match.group(1):
        x_obj = e.text.split(None, 1)[1]
        x_ov = x_obj.replace("-", "")
        if x_ov.isnumeric():
            x_obj = int(x_obj)
        try:
            x_user = await e.client.get_entity(x_obj)
        except (TypeError, ValueError) as x:
            return await e.reply(str(x))
    if isinstance(x_user, User):
        x_full = await e.client(GetFullUserRequest(x_user.username or x_user.id))
        out_str = "<b>User Info:</b>"
        out_str += f"\n<b>First Name:</b> {x_full.user.first_name}"
        if x_full.user.last_name:
            out_str += f"\n<b>Last Name:</b> {x_full.user.last_name}"
        if x_full.user.username:
            out_str += f"\n<b>Username:</b> @{x_full.user.username}"
        out_str += f"\n<b>User ID:</b> <code>{x_full.user.id}</code>"
        out_str += (
            f"\n<b>PermaLink:</b> <a href='tg://user?id={x_full.user.id}'>link</a>"
        )
        if x_full.profile_photo and x_full.profile_photo.dc_id:
            out_str += f"\n<b>DC ID:</b> {x_full.profile_photo.dc_id}"
        if x_full.about:
            out_str += f"\n\n<b>Bio:</b> <code>{x_full.about}</code>"
        if x_full.user.id == OWNER_ID:
            out_str += f"\n\nThis is my Master, he have total power over me!"
        out_str += f"\n\n<b>BlackListed:</b> No"
        await e.reply(out_str, file=x_full.profile_photo, parse_mode="html")
    if isinstance(x_user, Channel):
        x_channel = await e.client(GetFullChannelRequest(x_user.username or x_user.id))
        out_str = f"<b>Channel Info:</b>"
        out_str += f"\n<b>Title:</b> {x_user.title}"
        if x_user.username:
            out_str += f"\n<b>Username:</b> @{x_user.username}"
        out_str += f"\n<b>Chat ID:</b> <code>{x_user.id}</code>"
        if x_user.verified:
            out_str += "\n<b>Verified:</b> True"
        if x_channel.full_chat.about:
            out_str += f"\n\n<b>Bio:</b> <code>{x_channel.full_chat.about}</code>"
        if len(x_channel.chats) == 2:
            out_str += f"\n<b>Linked Chat:</b> {x_channel.chats[1].title}"
            out_str += (
                f"\n<b>Linked Chat ID:</b> <code>-100{x_channel.chats[1].id}</code>"
            )
        if x_channel.full_chat.participants_count > 999:
            participants_count = human_format(x_channel.full_chat.participants_count)
        else:
            participants_count = x_channel.full_chat.participants_count
        out_str += f"\n\n<b>Participants:</b> <code>{participants_count}"
        if x_channel.full_chat.admins_count:
            out_str += f"\n<b>Admins:</b> <code>{x_channel.full_chat.admins_count}"
        file = x_channel.full_chat.chat_photo
        if isinstance(file, PhotoEmpty):
            file = None
        await e.reply(out_str, file=file, parse_mode="html")


@Zbot(pattern="^/(stat|stat)(@Zaid2_Robot|@zaid2_robot)?$")
async def ___stat_chat__(e):
    for x in ["+stats", "/stats", "!stats", "?stats"]:
        if e.text.startswith(x):
            return
    __stats_format = translate(f"**Total Messages in {e.chat.title}:** `{e.id}`", e.chat_id)
    await e.reply(__stats_format)


__name__ = "Info"
__help__ = """
Here is the help menu for **info** module:
- /id `<user/chat/channel/forward>`: get the int id of the given entity.
- /info `<user/chat/channel>`: gather info about the given entity.
- /setbio `<text>`: set about bio of another user.
"""
CMD_HELP.update({__name__: [__name__, __help__]})
