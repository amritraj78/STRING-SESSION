import os
import sys
import time
import platform
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

import config
from config import OWNER_ID, START_TIME, get_readable_time
from StringGenBot.db.users import get_served_users
from StringGenBot.db.banned import add_banned_user, remove_banned_user, get_banned_users
from StringGenBot.ping import get_mem_usage


@Client.on_message(filters.user(OWNER_ID) & filters.command("ban"))
async def ban_user_handler(bot: Client, msg: Message):
    target_id = None
    if msg.reply_to_message and msg.reply_to_message.from_user:
        target_id = msg.reply_to_message.from_user.id
    elif len(msg.command) > 1:
        arg = msg.command[1]
        try:
            target_id = int(arg)
        except ValueError:
            try:
                user = await bot.get_users(arg)
                target_id = user.id
            except Exception:
                await msg.reply_text("❌ Invalid User ID or Username provided.")
                return

    if not target_id:
        await msg.reply_text("⚠️ **Usage:** `/ban <user_id/username>` or reply to a user's message.")
        return

    if target_id == OWNER_ID:
        await msg.reply_text("❌ You cannot ban the bot owner!")
        return

    await add_banned_user(target_id)
    await msg.reply_text(f"🚫 **User** `{target_id}` **has been banned successfully!**")


@Client.on_message(filters.user(OWNER_ID) & filters.command("unban"))
async def unban_user_handler(bot: Client, msg: Message):
    target_id = None
    if msg.reply_to_message and msg.reply_to_message.from_user:
        target_id = msg.reply_to_message.from_user.id
    elif len(msg.command) > 1:
        arg = msg.command[1]
        try:
            target_id = int(arg)
        except ValueError:
            try:
                user = await bot.get_users(arg)
                target_id = user.id
            except Exception:
                await msg.reply_text("❌ Invalid User ID or Username provided.")
                return

    if not target_id:
        await msg.reply_text("⚠️ **Usage:** `/unban <user_id/username>` or reply to a user's message.")
        return

    await remove_banned_user(target_id)
    await msg.reply_text(f"✅ **User** `{target_id}` **has been unbanned successfully!**")


@Client.on_message(filters.user(OWNER_ID) & filters.command("banned"))
async def banned_list_handler(bot: Client, msg: Message):
    banned = await get_banned_users()
    if not banned:
        await msg.reply_text("✨ **No users are currently banned.**")
        return

    text = f"🚫 **˹ 𝐁ᴀɴɴᴇᴅ 𝐔sᴇʀs ({len(banned)}) ˼**\n────────────────────────\n"
    for idx, uid in enumerate(banned[:50], 1):
        text += f"{idx}. `{uid}`\n"
    if len(banned) > 50:
        text += f"\n*...and {len(banned) - 50} more users.*"
    await msg.reply_text(text)


@Client.on_message(filters.user(OWNER_ID) & filters.command("stats"))
async def detailed_stats_handler(bot: Client, msg: Message):
    served_users = len(await get_served_users())
    banned_users = len(await get_banned_users())
    uptime = get_readable_time(time.time() - START_TIME)
    mem = get_mem_usage()
    py_ver = platform.python_version()

    text = (
        "📊 **˹ 𝐒ᴛʀɪɴɢ 𝐆ᴇɴ 𝐁ᴏᴛ — 𝐒ʏsᴛᴇᴍ 𝐃ᴀsʜʙᴏᴀʀᴅ ˼** 📊\n"
        "────────────────────────\n"
        f"👥 **ᴛᴏᴛᴀʟ sᴇʀᴠᴇᴅ ᴜsᴇʀs :** `{served_users}`\n"
        f"🚫 **ʙᴀɴɴᴇᴅ ᴜsᴇʀs :** `{banned_users}`\n"
        f"⏱️ **ʙᴏᴛ ᴜᴩᴛɪᴍᴇ :** `{uptime}`\n"
        f"💾 **ᴍᴇᴍᴏʀʏ ᴜsᴀɢᴇ :** `{mem}`\n"
        f"🐍 **ᴩʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{py_ver}`\n"
        f"🛰️ **ᴅᴀᴛᴀʙᴀsᴇ :** `{'MongoDB Connected ✅' if config.MONGO_DB_URI else 'In-Memory Cache ⚡'}`\n"
        f"🌐 **ᴋᴏʏᴇʙ ᴩᴏʀᴛ :** `{config.PORT}`\n"
        f"👑 **ᴏᴡɴᴇʀ ɪᴅ :** `{OWNER_ID}`\n"
        "────────────────────────"
    )
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🔄 ʀᴇғʀᴇsʜ", callback_data="refresh_stats"),
                InlineKeyboardButton("📢 ʙʀᴏᴀᴅᴄᴀsᴛ", callback_data="help_broadcast"),
            ]
        ]
    )
    await msg.reply_text(text, reply_markup=buttons)


@Client.on_message(filters.user(OWNER_ID) & filters.command(["restart", "reboot"]))
async def restart_bot_handler(bot: Client, msg: Message):
    await msg.reply_text("🔄 **ʀᴇsᴛᴀʀᴛɪɴɢ ʙᴏᴛ... ᴩʟᴇᴀsᴇ ᴡᴀɪᴛ ᴀ ғᴇᴡ sᴇᴄᴏɴᴅs.**")
    time.sleep(1)
    os.execl(sys.executable, sys.executable, *sys.argv)
