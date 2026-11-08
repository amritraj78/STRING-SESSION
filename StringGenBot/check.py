import re
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    AuthKeyUnregistered,
    UserDeactivated,
    SessionRevoked,
    AuthKeyDuplicated,
    RPCError,
)
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    AuthKeyUnregisteredError,
    UserDeactivatedError,
)

import config


def mask_phone(phone: str) -> str:
    if not phone:
        return "Hidden"
    clean = re.sub(r"[^\d+]", "", str(phone))
    if len(clean) >= 7:
        return clean[:4] + " ••••• " + clean[-2:]
    return clean[:2] + " •••• "


async def check_pyrogram_session(session_str: str):
    client = Client(
        name="session_check_pyro",
        api_id=config.API_ID,
        api_hash=config.API_HASH,
        session_string=session_str.strip(),
        in_memory=True,
    )
    try:
        await client.connect()
        me = await client.get_me()
        user_info = {
            "type": "Pyrogram",
            "id": me.id,
            "name": f"{me.first_name or ''} {me.last_name or ''}".strip() or "Unknown",
            "username": f"@{me.username}" if me.username else "None",
            "phone": mask_phone(me.phone_number),
            "premium": "Yes ⭐" if getattr(me, "is_premium", False) else "No",
            "dc_id": getattr(me, "dc_id", "N/A"),
            "is_bot": "Bot 🤖" if getattr(me, "is_bot", False) else "User 👤",
        }
        await client.disconnect()
        return True, user_info, None
    except (AuthKeyUnregistered, SessionRevoked):
        return False, None, "Session string has been terminated/revoked."
    except UserDeactivated:
        return False, None, "The Telegram account associated with this session is deleted/deactivated."
    except AuthKeyDuplicated:
        return False, None, "Auth key duplicated. Session cannot be used concurrently."
    except Exception as e:
        try:
            await client.disconnect()
        except Exception:
            pass
        return False, None, str(e)


async def check_telethon_session(session_str: str):
    client = TelegramClient(
        StringSession(session_str.strip()),
        config.API_ID,
        config.API_HASH,
    )
    try:
        await client.connect()
        if not await client.is_user_authorized():
            await client.disconnect()
            return False, None, "Session is not authorized or has expired."
        me = await client.get_me()
        user_info = {
            "type": "Telethon",
            "id": me.id,
            "name": f"{getattr(me, 'first_name', '') or ''} {getattr(me, 'last_name', '') or ''}".strip() or "Unknown",
            "username": f"@{me.username}" if getattr(me, "username", None) else "None",
            "phone": mask_phone(getattr(me, "phone", None)),
            "premium": "Yes ⭐" if getattr(me, "premium", False) else "No",
            "dc_id": "N/A",
            "is_bot": "Bot 🤖" if getattr(me, "bot", False) else "User 👤",
        }
        await client.disconnect()
        return True, user_info, None
    except (AuthKeyUnregisteredError, SessionPasswordNeededError if False else Exception) as e:
        try:
            await client.disconnect()
        except Exception:
            pass
        return False, None, str(e)


@Client.on_message(filters.command(["check", "check_session", "verify"]) & filters.private)
async def check_command(bot: Client, msg: Message):
    args = msg.text.split(None, 1)
    if len(args) > 1:
        session_str = args[1].strip()
    else:
        ask_msg = await bot.ask(
            msg.chat.id,
            "🔍 **ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ ᴘʏʀᴏɢʀᴀᴍ ᴏʀ ᴛᴇʟᴇᴛʜᴏɴ sᴇssɪᴏɴ sᴛʀɪɴɢ ᴛᴏ ᴄʜᴇᴄᴋ :**\n\n"
            "*(Your string is verified in-memory and will never be saved or shared)*",
            filters=filters.text,
            timeout=180,
        )
        if not ask_msg or not ask_msg.text:
            return
        if ask_msg.text.startswith("/"):
            await ask_msg.reply_text("❌ Verification cancelled.")
            return
        session_str = ask_msg.text.strip()

    status_msg = await msg.reply_text("🔎 **ᴠᴇʀɪғʏɪɴɢ sᴇssɪᴏɴ sᴛʀɪɴɢ...**")

    # Try Pyrogram first
    is_valid, info, err = await check_pyrogram_session(session_str)
    if not is_valid:
        # Try Telethon
        is_telethon_valid, telethon_info, telethon_err = await check_telethon_session(session_str)
        if is_telethon_valid:
            is_valid, info, err = True, telethon_info, None
        else:
            err = telethon_err or err

    if is_valid and info:
        text = (
            "✅ **˹ 𝐒ᴇssɪᴏɴ 𝐈s 𝐕ᴀʟɪᴅ & 𝐀ᴄᴛɪᴠᴇ ˼** ✅\n"
            "────────────────────────\n"
            f"👤 **ɴᴀᴍᴇ :** `{info['name']}`\n"
            f"🆔 **ᴜsᴇʀ ɪᴅ :** `{info['id']}`\n"
            f"🔗 **ᴜsᴇʀɴᴀᴍᴇ :** {info['username']}\n"
            f"📱 **ᴩʜᴏɴᴇ :** `{info['phone']}`\n"
            f"⭐ **ᴩʀᴇᴍɪᴜᴍ :** `{info['premium']}`\n"
            f"🏷️ **ᴀᴄᴄᴏᴜɴᴛ ᴛʏᴩᴇ :** `{info['is_bot']}`\n"
            f"⚡ **ᴇɴɢɪɴᴇ :** `{info['type']}`\n"
            f"🌐 **ᴅᴄ :** `{info['dc_id']}`\n"
            "────────────────────────\n"
            "🔒 *Verified securely in temporary memory.*"
        )
    else:
        text = (
            "❌ **˹ 𝐒ᴇssɪᴏɴ 𝐈s 𝐈ɴᴠᴀʟɪᴅ / 𝐄xᴘɪʀᴇᴅ ˼** ❌\n"
            "────────────────────────\n"
            f"⚠️ **ʀᴇᴀsᴏɴ :** `{err or 'Session string is corrupted or unauthorized.'}`\n\n"
            "👉 Please generate a fresh session string using /generate !"
        )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⚡ ɢᴇɴᴇʀᴀᴛᴇ ɴᴇᴡ sᴛʀɪɴɢ", callback_data="generate"),
                InlineKeyboardButton("🔍 ᴄʜᴇᴄᴋ ᴀɴᴏᴛʜᴇʀ", callback_data="check_session_btn"),
            ]
        ]
    )
    await status_msg.edit_text(text, reply_markup=buttons)
