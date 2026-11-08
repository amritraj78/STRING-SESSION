import time
import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import START_TIME, get_readable_time, OWNER_ID, SUPPORT_CHAT, CHANNEL


def get_mem_usage() -> str:
    try:
        with open("/proc/meminfo", "r") as f:
            lines = f.readlines()
        mem_total = 0
        mem_avail = 0
        for line in lines:
            if line.startswith("MemTotal:"):
                mem_total = int(line.split()[1])
            elif line.startswith("MemAvailable:"):
                mem_avail = int(line.split()[1])
        if mem_total > 0 and mem_avail > 0:
            used_mb = (mem_total - mem_avail) / 1024
            total_mb = mem_total / 1024
            pct = ((mem_total - mem_avail) / mem_total) * 100
            return f"{used_mb:.1f} MB / {total_mb:.1f} MB ({pct:.1f}%)"
    except Exception:
        pass
    return "N/A"


@Client.on_message(filters.command(["ping", "p"]) & filters.private)
async def ping_handler(bot: Client, msg: Message):
    start_time = time.time()
    sent_msg = await msg.reply_text("⚡ ᴘɪɴɢɪɴɢ...")
    end_time = time.time()
    latency = round((end_time - start_time) * 1000, 2)
    uptime_str = get_readable_time(time.time() - START_TIME)

    text = (
        f"📍 **ᴘᴏɴɢ !** `{latency} ᴍs`\n\n"
        f"⏱️ **ᴜᴩᴛɪᴍᴇ :** `{uptime_str}`\n"
        f"🤖 **ʙᴏᴛ sᴛᴀᴛᴜs :** `ᴀᴄᴛɪᴠᴇ & sᴛᴀʙʟᴇ` ✅"
    )
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🔄 ʀᴇғʀᴇsʜ", callback_data="refresh_ping"),
                InlineKeyboardButton("🥀 sᴜᴩᴩᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT.lstrip('@')}"),
            ]
        ]
    )
    await sent_msg.edit_text(text, reply_markup=buttons)


@Client.on_message(filters.command(["alive", "uptime"]) & filters.private)
async def alive_handler(bot: Client, msg: Message):
    uptime_str = get_readable_time(time.time() - START_TIME)
    mem_info = get_mem_usage()
    bot_username = (await bot.get_me()).username or "String_rebot"

    alive_text = (
        "✨ **˹ 𝐒ᴛʀɪɴɢ 𝐒ᴇssɪᴏɴ 𝐁ᴏᴛ ɪs 𝐀ʟɪᴠᴇ ˼** ✨\n"
        "────────────────────────\n"
        f"🤖 **ʙᴏᴛ ɴᴀᴍᴇ :** @{bot_username}\n"
        f"⏱️ **ᴜᴩᴛɪᴍᴇ :** `{uptime_str}`\n"
        f"💾 **ᴍᴇᴍᴏʀʏ :** `{mem_info}`\n"
        f"🛰️ **ᴇɴɢɪɴᴇ :** `ᴘʏʀᴏɢʀᴀᴍ + ᴛᴇʟᴇᴛʜᴏɴ`\n"
        f"👑 **ᴏᴡɴᴇʀ :** [ᴛʜᴇ ᴠɪᴘ ʙᴏʏ](tg://user?id={OWNER_ID})\n"
        "────────────────────────\n"
        "⚡ *𝐅𝐮𝐥𝐥𝐲 𝐒𝐞𝐜𝐮𝐫𝐞 & 𝐎𝐩𝐞𝐫𝐚𝐭𝐢𝐨𝐧𝐚𝐥 𝟐𝟒/𝟕*"
    )
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⚡ ɢᴇɴᴇʀᴀᴛᴇ sᴛʀɪɴɢ ⚡", callback_data="generate"),
            ],
            [
                InlineKeyboardButton("❣️ sᴜᴩᴩᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT.lstrip('@')}"),
                InlineKeyboardButton("🥀 ᴏғғɪᴄᴇ", url=f"https://t.me/{CHANNEL.lstrip('@')}"),
            ],
        ]
    )
    await msg.reply_text(alive_text, reply_markup=buttons, disable_web_page_preview=True)
