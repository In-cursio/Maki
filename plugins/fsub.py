import asyncio
from pyrogram import Client, enums, filters
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from database.fsub_db import FSub
from database.req_filesdb import ReqFiles
from info import ADMINS

from logging import getLogger

logger = getLogger(__name__)
INVITE_LINK = None
db = FSub
req_db = ReqFiles


async def ForceSub(bot: Client, update: Message, file_id: str = False, mode="checksub"):
    global INVITE_LINK
    auth = ADMINS
    if update.from_user.id in auth:
        return True

    req_cnl = await db().get_req_channel()
    fsub_cnl = await db().get_auth_channel()
    if not fsub_cnl and not req_cnl:
        return True

    is_cb = False
    if not hasattr(update, "chat"):
        update.message.from_user = update.from_user
        update = update.message
        is_cb = True

    # Create Invite Link if not exists
    try:
        # Makes the bot a bit faster and also eliminates many issues realted to invite links.
        if INVITE_LINK is None:
            invite_link = (
                await bot.create_chat_invite_link(
                    chat_id=(int(fsub_cnl) if not req_cnl and not req_cnl else req_cnl),
                    creates_join_request=True if req_cnl else False,
                )
            ).invite_link
            INVITE_LINK = invite_link
            logger.info("Created Req link")
        else:
            invite_link = INVITE_LINK

    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, update, file_id)
        return fix_

    except Exception as err:
        print(f"Unable to do Force Subscribe to {req_cnl}\n\nError: {err}\n\n")
        await update.reply(
            text="Something went Wrong.",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
        return False

    # Mian Logic
    if req_cnl and db().isActive():
        try:
            # Check if User is Requested to Join Channel
            user = await db().get_user(user_id=update.from_user.id, req_channel=req_cnl)
            if user and user["user_id"] == update.from_user.id:
                return True
        except Exception as e:
            logger.exception(e, exc_info=True)
            await update.reply(
                text="Something went Wrong.",
                parse_mode=enums.ParseMode.MARKDOWN,
                disable_web_page_preview=True,
            )
            return False

    try:
        if not fsub_cnl:
            raise UserNotParticipant
        # Check if User is Already Joined Channel
        user = await bot.get_chat_member(
            chat_id = (int(fsub_cnl) if not req_cnl else req_cnl),
            user_id=update.from_user.id,
        )
        if user.status == "kicked":
            await bot.send_message(
                chat_id=update.from_user.id,
                text="Sorry Sir, You are Banned to use me.",
                parse_mode=enums.ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_to_message_id=update.message_id,
            )
            return False

        else:
            return True
    except UserNotParticipant:
        text = """**Please Join My Updates Channel to use this Bot!**"""

        buttons = [
            [InlineKeyboardButton("📢 Request to Join Channel 📢", url=invite_link)],
            [
                InlineKeyboardButton(
                    "🤔 Hᴇʏ Bᴏᴛ....! Wʜʏ I'ᴍ Jᴏɪɴɪɴɢ",
                    url="https://graph.org/W%CA%9C%CA%8F-I%E1%B4%8D-J%E1%B4%8F%C9%AA%C9%B4%C9%AA%C9%B4%C9%A2-01-07",
                )
            ],
        ]

        if file_id is False:
            buttons.pop()

        if not is_cb:
            await req_db().add_file(
                user_id=update.from_user.id,
                group_id=req_cnl,
                file_mode=mode,
                file_id=file_id,
            )
            await update.reply(
                text=text,
                quote=True,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=enums.ParseMode.MARKDOWN,
            )
        return False

    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, update, file_id)
        return fix_

    except Exception as err:
        print(f"Something Went Wrong! Unable to do Force Subscribe.\nError: {err}")
        await update.reply(
            text="Something went Wrong.",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
        return False


def set_global_invite(url: str):
    global INVITE_LINK
    INVITE_LINK = url


@Client.on_message(filters.command("addfsub") & filters.user(ADMINS), group=1)
async def add_channel(client, message):
    if len(message.command) < 2:
        await message.reply("Usage: /addfsub <channel_id>")
        return
    try:
        channel_id = int(message.command[1])
        add = await db().add_auth_channel(auth_channel=channel_id)
        if add:
            await message.reply(f"Fsub channel `{channel_id}` added successfully.")
        else:
            await message.reply("Unable to update Fsub channel.")
    except ValueError:
        await message.reply("Please provide a valid channel ID.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")


@Client.on_message(filters.command("addreq") & filters.user(ADMINS), group=1)
async def add_req_channel(client, message):
    if len(message.command) < 2:
        await message.reply("Usage: /addreq <channel_id>")
        return
    try:
        channel_id = int(message.command[1])
        add = await db().add_req_channel(req_channel=channel_id)
        if add:
            await message.reply(f"Request channel `{channel_id}` added successfully.")
        else:
            await message.reply("Unable to update request channel.")
    except ValueError:
        await message.reply("Please provide a valid channel ID.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")


@Client.on_message(filters.command("delfsub") & filters.user(ADMINS), group=1)
async def del_fsub_channel(client, message):
    if len(message.command) < 2:
        await message.reply("Usage: /delfsub <channel_id>")
        return
    try:
        channel_id = int(message.command[1])
        add = await db().delete_auth_channel(channel_id)
        if add:
            await message.reply(f"Fsub channel `{channel_id}` deleted successfully.")
        else:
            await message.reply("Unable to delete Fsub channel.")
    except ValueError:
        await message.reply("Please provide a valid channel ID.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")


@Client.on_message(filters.command("delreq") & filters.user(ADMINS), group=1)
async def del_req_channel(client, message):
    if len(message.command) < 2:
        await message.reply("Usage: /delreq <channel_id>")
        return
    try:
        channel_id = int(message.command[1])
        add = await db().delete_req_channel(channel_id)
        if add:
            await message.reply(f"Request channel `{channel_id}` deleted successfully.")
        else:
            await message.reply("Unable to delete Request channel.")
    except ValueError:
        await message.reply("Please provide a valid channel ID.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")


@Client.on_message(filters.command("getsub") & filters.user(ADMINS), group=1)
async def get_sub_channel(client, message):
    try:
        req = await db().get_req_channel()
        if req:
            await message.reply(f"Request channel ID: `{req}` ")
            return
        auth = await db().get_auth_channel()
        if auth:
            await message.reply(f"Auth channel ID: `{auth}` ")
            return
        await message.reply("No Fsub/Request channel found.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")
