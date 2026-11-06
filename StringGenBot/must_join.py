import time
from config import MUST_JOIN

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden

# In-memory TTL cache for verified members (10 minutes TTL)
_JOIN_CACHE = {}  # {user_id: timestamp}
_CACHE_TTL = 600

# Cache resolved links so get_chat is not called repeatedly
_LINK_CACHE = {}  # {target: (link, label)}


def is_user_verified(user_id: int) -> bool:
    verified_at = _JOIN_CACHE.get(user_id)
    if verified_at and (time.time() - verified_at) < _CACHE_TTL:
        return True
    return False


def set_user_verified(user_id: int):
    _JOIN_CACHE[user_id] = time.time()


@Client.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(bot: Client, msg: Message):
    if not MUST_JOIN:
        return
    if not msg.from_user:
        return

    user_id = msg.from_user.id

    # Fast-path: bypass API calls if user was recently verified
    if is_user_verified(user_id):
        return

    raw_targets = [t.strip() for t in MUST_JOIN.replace(",", " ").split() if t.strip()]
    if not raw_targets:
        return

    buttons = []
    unjoined = False

    for target in raw_targets:
        try:
            try:
                await bot.get_chat_member(target, user_id)
            except UserNotParticipant:
                unjoined = True
                if target in _LINK_CACHE:
                    link, label = _LINK_CACHE[target]
                else:
                    if target.startswith("https://") or target.startswith("http://"):
                        link = target
                        label = "𝐉𝐎𝐈𝐍"
                    elif target.startswith("-100"):
                        try:
                            chat_info = await bot.get_chat(int(target))
                            link = chat_info.invite_link or (f"https://t.me/{chat_info.username}" if chat_info.username else None)
                            label = chat_info.title or "𝐉𝐎𝐈𝐍"
                        except Exception:
                            link = None
                            label = "𝐉𝐎𝐈𝐍"
                    else:
                        channel_user = target.lstrip("@")
                        link = f"https://t.me/{channel_user}"
                        label = f"» 𝐉𝐎𝐈𝐍 @{channel_user} «"

                    if link:
                        _LINK_CACHE[target] = (link, label)

                if link:
                    buttons.append([InlineKeyboardButton(label, url=link)])
        except ChatAdminRequired:
            print(f"Promote me as an admin in the chat : {target} !")
        except Exception as e:
            print(f"Must join error for {target}: {e}")

    if unjoined and buttons:
        try:
            await msg.reply_photo(
                photo="https://files.catbox.moe/h75qko.jpg",
                caption="» 𝐅𝐈𝐑𝐒𝐓𝐋𝐘 𝐘𝐎𝐔 𝐍𝐄𝐄𝐃 𝐓𝐎 𝐉𝐎𝐈𝐍 𝐎𝐔𝐑 𝐅𝐀𝐌𝐈𝐋𝐘 𝐓𝐎 𝐔𝐒𝐄 𝐓𝐇𝐈𝐒 𝐁𝐎𝐓.\n𝐀𝐅𝐓𝐄𝐑 𝐉𝐎𝐈𝐍𝐈𝐍𝐆, 𝐒𝐓𝐀𝐑𝐓 𝐌𝐄 𝐀𝐆𝐀𝐈𝐍 !",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            await msg.stop_propagation()
        except ChatWriteForbidden:
            pass
    else:
        # User is verified across all required targets
        set_user_verified(user_id)
