from logging import getLogger
from pyrogram import Client, filters, enums
from pyrogram.types import ChatJoinRequest
from database.fsub_db import FSub
from database.req_filesdb import ReqFiles
from info import ADMINS, CUSTOM_FILE_CAPTION
from database.ia_filterdb import get_file_details
from utils import get_size

db = FSub
req_db = ReqFiles
logger = getLogger(__name__)


@Client.on_chat_join_request()
async def join_reqs(client, join_req: ChatJoinRequest):
    if db().isActive():
        req_cnl = await db().get_req_channel()
        if req_cnl:
            if join_req.chat.id == req_cnl:
                req_channel = join_req.chat.id
                user_id = join_req.from_user.id
                first_name = join_req.from_user.first_name
                username = join_req.from_user.username
                date = join_req.date

                await db().add_user(
                    req_channel=req_channel,
                    user_id=user_id,
                    first_name=first_name,
                    username=username,
                    date=date,
                )

                file = await req_db().get_file(user_id, req_cnl)
                if file:
                    file_id = file.get("file_id")
                    mode = file.get("mode")
                    files_ = await get_file_details(file_id)
                    if not files_:
                        return await client.send_message(user_id, "No such file exist.")
                    files = files_[0]
                    title = files.file_name
                    size = get_size(files.file_size)
                    # f_caption = files.caption if files.caption else None
                    f_caption = "@"+client.me.username
                    if CUSTOM_FILE_CAPTION:
                        try:
                            f_caption = CUSTOM_FILE_CAPTION.format(
                                file_name="" if title is None else title,
                                file_size="" if size is None else size,
                                file_caption="" if f_caption is None else f_caption,
                            )
                        except Exception as e:
                            logger.exception(e)
                            f_caption = f_caption
                    if f_caption is None:
                        f_caption = f"{title}"
                    file_send = await client.send_cached_media(
                        chat_id=user_id,
                        file_id=file_id,
                        caption=f_caption,
                        protect_content=True if mode == "checksubp" else False,
                    )
                    await req_db().delete_file(user_id, req_cnl)


@Client.on_message(
    filters.command("totalrequests") & filters.private & filters.user(ADMINS), group=1
)
async def total_requests(client, message):
    if db().isActive():
        req_cnl = await db().get_req_channel()
        total = await db().get_all_users_count(req_cnl)
        await message.reply_text(
            text=f"Total Requests: {total}",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )


@Client.on_message(
    filters.command("purgerequests") & filters.private & filters.user(ADMINS), group=1
)
async def purge_requests(client, message):
    if db().isActive():
        req_cnl = await db().get_req_channel()
        await db().delete_all_users(req_cnl)
        await message.reply_text(
            text="Purged All Requests.",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )


@Client.on_message(
    filters.command("purgefiles") & filters.private & filters.user(ADMINS), group=1
)
async def purge_files(client, message):
    if req_db().isActive():
        del_f = await req_db.delete_all_files()
        if del_f:
            await message.reply_text(
                text="Purged All Request Files.",
            )
        else:
            await message.reply_text(
                text="No Files Found.",
            )
