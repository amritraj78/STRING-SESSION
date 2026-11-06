from config import MUST_JOIN

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden


@Client.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(bot: Client, msg: Message):
    if not MUST_JOIN:
        return
    if not msg.from_user:
        return
    try:
        try:
            await bot.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            target = MUST_JOIN.strip()
            if target.startswith("https://") or target.startswith("http://"):
                link = target
            elif target.startswith("-100"):
                try:
                    chat_info = await bot.get_chat(int(target))
                    link = chat_info.invite_link or (f"https://t.me/{chat_info.username}" if chat_info.username else None)
                except Exception:
                    link = None
            else:
                channel_user = target.lstrip("@")
                link = f"https://t.me/{channel_user}"

            if not link:
                return

            try:
                await msg.reply_photo(
                    photo="https://files.catbox.moe/h75qko.jpg",
                    caption=f"» 𝐅𝐈𝐑𝐒𝐓𝐋𝐘 𝐘𝐎𝐔 𝐍𝐄𝐄𝐃 𝐓𝐎 𝐉𝐎𝐈𝐍 𝐎𝐔𝐑 𝐅𝐀𝐌𝐈𝐋𝐘 𝐓𝐇𝐄𝐍 𝐘𝐎𝐔 𝐂𝐀𝐍 𝐔𝐒𝐄 𝐌𝐄 [𝐎𝐅𝐅𝐈𝐂𝐄]({link}). 𝐀𝐅𝐓𝐄𝐑 𝐉𝐎𝐈𝐍 𝐒𝐓𝐀𝐑𝐓 𝐌𝐄 𝐀𝐆𝐀𝐈𝐍 !",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("</> 𝐎𝐅𝐅𝐈𝐂𝐄", url=link),
                            ]
                        ]
                    ),
                )
                await msg.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        print(f"Promote me as an admin in the MUST_JOIN chat : {MUST_JOIN} !")
    except Exception as e:
        print(f"Must join error: {e}")
