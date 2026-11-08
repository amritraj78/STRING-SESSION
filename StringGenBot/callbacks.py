import time
import traceback
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

import config
from config import OWNER_ID, START_TIME, get_readable_time, SUPPORT_CHAT, CHANNEL
from StringGenBot.generate import generate_session, ask_ques, buttons_ques
from StringGenBot.start import START_MARKUP, HELP_MARKUP, ABOUT_MARKUP, get_start_text, get_help_text, get_about_text
from StringGenBot.ping import get_mem_usage
from StringGenBot.db.users import get_served_users
from StringGenBot.db.banned import get_banned_users


ADMIN_HELP_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("📊 ᴠɪᴇᴡ sᴛᴀᴛs", callback_data="refresh_stats"),
            InlineKeyboardButton("📢 ʙʀᴏᴀᴅᴄᴀsᴛ ɢᴜɪᴅᴇ", callback_data="help_broadcast"),
        ],
        [
            InlineKeyboardButton("🔙 ʙᴀᴄᴋ ᴛᴏ ʜᴇʟᴩ", callback_data="help_menu"),
        ],
    ]
)


@Client.on_callback_query()
async def _callbacks(bot: Client, callback_query: CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id

    if data == "start_menu":
        await callback_query.answer()
        me2 = bot.me.mention if getattr(bot, "me", None) else (await bot.get_me()).mention
        text = get_start_text(callback_query.from_user.mention, me2)
        try:
            await callback_query.message.edit_text(text, reply_markup=START_MARKUP, disable_web_page_preview=True)
        except Exception:
            pass

    elif data == "help_menu":
        await callback_query.answer()
        try:
            await callback_query.message.edit_text(get_help_text(), reply_markup=HELP_MARKUP)
        except Exception:
            pass

    elif data == "about_menu":
        await callback_query.answer()
        try:
            await callback_query.message.edit_text(get_about_text(), reply_markup=ABOUT_MARKUP)
        except Exception:
            pass

    elif data == "admin_help":
        await callback_query.answer()
        if user_id != OWNER_ID:
            await callback_query.answer("⚠️ Only the bot owner can view admin commands.", show_alert=True)
            return
        admin_text = (
            "👑 **˹ 𝐎ᴡɴᴇʀ 𝐀ᴅᴍɪɴ 𝐂ᴏᴍᴍᴀɴᴅs ˼** 👑\n"
            "────────────────────────\n"
            "• `/broadcast` - Broadcast message to all users (reply to message)\n"
            "• `/broadcast -pin` - Broadcast and pin in user's DM\n"
            "• `/broadcast -copy` - Broadcast as clean copy\n"
            "• `/stats` - Detailed system and database analytics\n"
            "• `/ban <id>` - Ban user from using bot\n"
            "• `/unban <id>` - Unban user\n"
            "• `/banned` - List all banned users\n"
            "• `/restart` - Restart bot process\n"
            "• `/eval <code>` - Execute Python expression (developer)\n"
            "• `/sh <cmd>` - Execute bash terminal command\n"
            "────────────────────────"
        )
        try:
            await callback_query.message.edit_text(admin_text, reply_markup=ADMIN_HELP_MARKUP)
        except Exception:
            pass

    elif data == "help_broadcast":
        await callback_query.answer()
        broadcast_guide = (
            "📢 **˹ 𝐁ʀᴏᴀᴅᴄᴀsᴛ 𝐆ᴜɪᴅᴇ ˼** 📢\n"
            "────────────────────────\n"
            "**How to use broadcast:**\n"
            "1. Send or forward any message to the bot (text, sticker, image, video, document).\n"
            "2. Reply to that message with `/broadcast`.\n\n"
            "**Optional Flags:**\n"
            "• `/broadcast -copy` - Sends without 'Forwarded from' header.\n"
            "• `/broadcast -pin` - Pins the broadcasted message in users' DM.\n"
            "• `/broadcast -copy -pin` - Clean copy + pin message."
        )
        try:
            await callback_query.message.edit_text(
                broadcast_guide,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 ʙᴀᴄᴋ", callback_data="admin_help")]]),
            )
        except Exception:
            pass

    elif data == "check_session_btn":
        await callback_query.answer()
        await callback_query.message.reply_text(
            "🔍 **ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ ᴘʏʀᴏɢʀᴀᴍ ᴏʀ ᴛᴇʟᴇᴛʜᴏɴ sᴇssɪᴏɴ sᴛʀɪɴɢ :**\n\n"
            "*(Or use command `/check <your_session_string>`)*",
        )

    elif data == "refresh_ping":
        start_time = time.time()
        await callback_query.answer("Pinging...")
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
        try:
            await callback_query.message.edit_text(text, reply_markup=buttons)
        except Exception:
            pass

    elif data == "refresh_stats":
        await callback_query.answer("Refreshing stats...")
        served_users = len(await get_served_users())
        banned_users = len(await get_banned_users())
        uptime = get_readable_time(time.time() - START_TIME)
        mem = get_mem_usage()
        text = (
            "📊 **˹ 𝐒ᴛʀɪɴɢ 𝐆ᴇɴ 𝐁ᴏᴛ — 𝐒ʏsᴛᴇᴍ 𝐃ᴀsʜʙᴏᴀʀᴅ ˼** 📊\n"
            "────────────────────────\n"
            f"👥 **ᴛᴏᴛᴀʟ sᴇʀᴠᴇᴅ ᴜsᴇʀs :** `{served_users}`\n"
            f"🚫 **ʙᴀɴɴᴇᴅ ᴜsᴇʀs :** `{banned_users}`\n"
            f"⏱️ **ʙᴏᴛ ᴜᴩᴛɪᴍᴇ :** `{uptime}`\n"
            f"💾 **ᴍᴇᴍᴏʀʏ ᴜsᴀɢᴇ :** `{mem}`\n"
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
        try:
            await callback_query.message.edit_text(text, reply_markup=buttons)
        except Exception:
            pass

    elif data == "generate":
        await callback_query.answer()
        await callback_query.message.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))

    elif data.startswith("pyrogram") or data.startswith("telethon"):
        try:
            if data == "pyrogram":
                await callback_query.answer()
                await generate_session(bot, callback_query.message)
            elif data == "pyrogram1":
                await callback_query.answer()
                await generate_session(bot, callback_query.message, old_pyro=True)
            elif data == "pyrogram_bot":
                await callback_query.answer("» ᴛʜᴇ sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴇᴅ ᴡɪʟʟ ʙᴇ ᴏғ ᴩʏʀᴏɢʀᴀᴍ ᴠ2.", show_alert=True)
                await generate_session(bot, callback_query.message, is_bot=True)
            elif data == "telethon_bot":
                await callback_query.answer()
                await generate_session(bot, callback_query.message, telethon=True, is_bot=True)
            elif data == "telethon":
                await callback_query.answer()
                await generate_session(bot, callback_query.message, telethon=True)
        except Exception as e:
            print(traceback.format_exc())
            print(e)
            error_msg = (
                "ᴡᴛғ ! sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ. \n\n**ᴇʀʀᴏʀ** : {} \n\n"
                f"**ᴩʟᴇᴀsᴇ ғᴏʀᴡᴀʀᴅ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴛᴏ @{config.SUPPORT_CHAT.lstrip('@')}**, ɪғ ᴛʜɪs ᴍᴇssᴀɢᴇ "
                "ᴅᴏᴇsɴ'ᴛ ᴄᴏɴᴛᴀɪɴ ᴀɴʏ sᴇɴsɪᴛɪᴠᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ʙᴇᴄᴀᴜsᴇ ᴛʜɪs ᴇʀʀᴏʀ ɪs **ɴᴏᴛ ʟᴏɢɢᴇᴅ ʙʏ ᴛʜᴇ ʙᴏᴛ** !"
            )
            await callback_query.message.reply(error_msg.format(str(e)))
