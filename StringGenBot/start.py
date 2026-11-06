from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from config import OWNER_ID, SUPPORT_CHAT, CHANNEL


def filter(cmd: str):
    return filters.private & filters.incoming & filters.command(cmd)


@Client.on_message(filter("start"))
async def start(bot: Client, msg: Message):
    me2 = bot.me.mention if getattr(bot, "me", None) else (await bot.get_me()).mention
    support_url = SUPPORT_CHAT if SUPPORT_CHAT.startswith("http") else f"https://t.me/{SUPPORT_CHAT.lstrip('@')}"
    channel_url = CHANNEL if CHANNEL.startswith("http") else f"https://t.me/{CHANNEL.lstrip('@')}"

    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"""𝐇𝐞𝐲 {msg.from_user.mention}🍷,

𝐈 𝐀𝐦 {me2},
𝐓𝐑𝐔𝐒𝐓𝐄𝐃 𝐒𝐓𝐑𝐈𝐍𝐆 𝐆𝐄𝐍𝐄𝐑𝐀𝐓𝐎𝐑 𝐁𝐎𝐓.
𝐅𝐔𝐋𝐋𝐘 𝐒𝐀𝐅𝐄 & 𝐒𝐄𝐂𝐔𝐑𝐄.
𝐍𝐎 𝐀𝐌𝐘 𝐄𝐑𝐑𝐎𝐑.

𝐌𝐚𝐝𝐞 𝐁𝐲  : [𝐓𝐇𝐄 𝐕𝐈𝐏 𝐁𝐎𝐘](tg://user?id={OWNER_ID}) !""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="⚡𝐆𝐄𝐍𝐄𝐑𝐀𝐓𝐄 𝐒𝐓𝐑𝐈𝐍𝐆⚡", callback_data="generate")
                ],
                [
                    InlineKeyboardButton("❣️ 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 ❣️", url=support_url),
                    InlineKeyboardButton("🥀 𝐎𝐟𝐟𝐢𝐜𝐞 🥀", url=channel_url),
                ],
            ]
        ),
        disable_web_page_preview=True,
    )
