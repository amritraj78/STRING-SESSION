import asyncio
import time
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, RPCError

from config import OWNER_ID, get_readable_time
from StringGenBot.db.users import get_served_users


@Client.on_message(filters.user(OWNER_ID) & filters.command(["broadcast", "gcast"]))
async def broadcast_handler(bot: Client, msg: Message):
    if not msg.reply_to_message:
        await msg.reply_text(
            "⚠️ **ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ!**\n\n"
            "**Usᴀɢᴇ :**\n"
            "• `/broadcast` - Forward message with source quote\n"
            "• `/broadcast -copy` - Send clean copy without forward quote\n"
            "• `/broadcast -pin` - Send and pin in user's DM\n"
            "• `/broadcast -copy -pin` - Clean copy + pin"
        )
        return

    users = await get_served_users()
    total_users = len(users)
    if total_users == 0:
        await msg.reply_text("❌ No users found in database to broadcast to.")
        return

    status_msg = await msg.reply_text(
        f"📢 **sᴛᴀʀᴛɪɴɢ ʙʀᴏᴀᴅᴄᴀsᴛ ᴛᴏ {total_users} ᴜsᴇʀs...**"
    )

    args = msg.text.lower().split()
    pin = "-pin" in args
    as_copy = "-copy" in args
    target_msg = msg.reply_to_message

    sent = 0
    blocked = 0
    deleted = 0
    failed = 0
    start_time = time.time()

    for idx, user in enumerate(users):
        user_id = user.get("user_id") if isinstance(user, dict) else user
        if not user_id or user_id == OWNER_ID:
            continue

        try:
            if as_copy:
                m = await target_msg.copy(chat_id=user_id)
            else:
                m = await target_msg.forward(chat_id=user_id)

            if pin and m:
                try:
                    await m.pin(both_sides=True)
                except Exception:
                    pass
            sent += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                if as_copy:
                    m = await target_msg.copy(chat_id=user_id)
                else:
                    m = await target_msg.forward(chat_id=user_id)
                if pin and m:
                    try:
                        await m.pin(both_sides=True)
                    except Exception:
                        pass
                sent += 1
            except Exception:
                failed += 1
        except UserIsBlocked:
            blocked += 1
        except InputUserDeactivated:
            deleted += 1
        except Exception:
            failed += 1

        # Update progress every 25 users
        if (idx + 1) % 25 == 0 or (idx + 1) == total_users:
            try:
                elapsed = round(time.time() - start_time, 1)
                await status_msg.edit_text(
                    f"📢 **ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ...**\n\n"
                    f"👥 **ᴘʀᴏɢʀᴇss :** `{idx + 1}/{total_users}`\n"
                    f"✅ **sᴇɴᴛ :** `{sent}`\n"
                    f"🚫 **ʙʟᴏᴄᴋᴇᴅ :** `{blocked}`\n"
                    f"💀 **ᴅᴇʟᴇᴛᴇᴅ :** `{deleted}`\n"
                    f"⏱️ **ᴛɪᴍᴇ :** `{elapsed}s`"
                )
            except Exception:
                pass

        await asyncio.sleep(0.05)

    duration = get_readable_time(time.time() - start_time)
    final_text = (
        "✅ **˹ 𝐁ʀᴏᴀᴅᴄᴀsᴛ 𝐂ᴏᴍᴘʟᴇᴛᴇᴅ ˼**\n"
        "────────────────────────\n"
        f"👥 **ᴛᴏᴛᴀʟ ᴜsᴇʀs :** `{total_users}`\n"
        f"✅ **sᴜᴄᴄᴇssғᴜʟʟʏ sᴇɴᴛ :** `{sent}`\n"
        f"🚫 **ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs :** `{blocked}`\n"
        f"💀 **ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ :** `{deleted}`\n"
        f"⚠️ **ғᴀɪʟᴇᴅ :** `{failed}`\n"
        f"⏱️ **ᴛᴏᴛᴀʟ ᴛɪᴍᴇ :** `{duration}`\n"
        "────────────────────────"
    )
    await status_msg.edit_text(final_text)
