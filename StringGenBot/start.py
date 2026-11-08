from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from config import OWNER_ID, SUPPORT_CHAT, CHANNEL

_SUPPORT_URL = SUPPORT_CHAT if SUPPORT_CHAT.startswith("http") else f"https://t.me/{SUPPORT_CHAT.lstrip('@')}"
_CHANNEL_URL = CHANNEL if CHANNEL.startswith("http") else f"https://t.me/{CHANNEL.lstrip('@')}"

START_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="⚡ ɢᴇɴᴇʀᴀᴛᴇ sᴛʀɪɴɢ ⚡", callback_data="generate")
        ],
        [
            InlineKeyboardButton(text="🔍 ᴠᴇʀɪғʏ sᴇssɪᴏɴ", callback_data="check_session_btn"),
            InlineKeyboardButton(text="⚡ ᴘɪɴɢ / sᴛᴀᴛs", callback_data="refresh_ping"),
        ],
        [
            InlineKeyboardButton(text="📖 ʜᴇʟᴘ & ᴄᴍᴅs", callback_data="help_menu"),
            InlineKeyboardButton(text="ℹ️ ᴀʙᴏᴜᴛ ʙᴏᴛ", callback_data="about_menu"),
        ],
        [
            InlineKeyboardButton("❣️ sᴜᴩᴩᴏʀᴛ", url=_SUPPORT_URL),
            InlineKeyboardButton("🥀 ᴏғғɪᴄᴇ", url=_CHANNEL_URL),
        ],
    ]
)

HELP_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("⚡ ɢᴇɴᴇʀᴀᴛᴇ", callback_data="generate"),
            InlineKeyboardButton("🔍 ᴠᴇʀɪғʏ", callback_data="check_session_btn"),
        ],
        [
            InlineKeyboardButton("👑 ᴀᴅᴍɪɴ ᴄᴍᴅs", callback_data="admin_help"),
            InlineKeyboardButton("ℹ️ ᴀʙᴏᴜᴛ", callback_data="about_menu"),
        ],
        [
            InlineKeyboardButton("🔙 ʙᴀᴄᴋ ᴛᴏ ᴍᴇɴᴜ", callback_data="start_menu"),
        ],
    ]
)

ABOUT_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("❣️ sᴜᴩᴩᴏʀᴛ ɢʀᴏᴜᴘ", url=_SUPPORT_URL),
            InlineKeyboardButton("🥀 ᴜᴩᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ", url=_CHANNEL_URL),
        ],
        [
            InlineKeyboardButton("🔙 ʙᴀᴄᴋ ᴛᴏ ᴍᴇɴᴜ", callback_data="start_menu"),
        ],
    ]
)


def get_start_text(mention: str, bot_mention: str) -> str:
    return (
        f"𝐇𝐞𝐲 {mention} 🍷,\n\n"
        f"𝐈 𝐀𝐦 {bot_mention},\n"
        "✨ **ᴛʀᴜsᴛᴇᴅ sᴛʀɪɴɢ sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴏʀ ʙᴏᴛ** ✨\n"
        "────────────────────────\n"
        "🚀 **𝐅𝐄𝐀𝐓𝐔𝐑𝐄𝐒 :**\n"
        "• ⚡ Generate Pyrogram v1, v2 & Telethon\n"
        "• 🤖 Generate Bot Tokens & String Sessions\n"
        "• 🔍 In-memory Session String Validator\n"
        "• 🔒 100% Secure & Zero Database Logging\n"
        "• 🌐 24/7 High-speed Cloud Deployment\n"
        "────────────────────────\n"
        f"👑 **𝐌𝐚𝐝𝐞 𝐁𝐲 :** [ᴛʜᴇ ᴠɪᴘ ʙᴏʏ](tg://user?id={OWNER_ID})"
    )


def get_help_text() -> str:
    return (
        "📖 **˹ 𝐒ᴛʀɪɴɢ 𝐆ᴇɴ 𝐁ᴏᴛ — 𝐇ᴇʟᴩ 𝐌ᴇɴᴜ ˼** 📖\n"
        "────────────────────────\n"
        "⚡ **ᴜsᴇʀ ᴄᴏᴍᴍᴀɴᴅs :**\n"
        "• `/start` - Start the bot & view main menu\n"
        "• `/generate` - Launch session generator\n"
        "• `/check` - Verify if a session string is valid\n"
        "• `/ping` - Check bot response latency & uptime\n"
        "• `/alive` or `/uptime` - View server system status\n"
        "• `/help` - View this help guide\n"
        "• `/about` - View bot & developer information\n\n"
        "💡 *Click below to view Admin commands or start generating!*"
    )


def get_about_text() -> str:
    return (
        "ℹ️ **˹ 𝐀ʙᴏᴜᴛ 𝐒ᴛʀɪɴɢ 𝐒ᴇssɪᴏɴ 𝐁ᴏᴛ ˼** ℹ️\n"
        "────────────────────────\n"
        "🤖 **ʙᴏᴛ ɴᴀᴍᴇ :** String Session Generator\n"
        "🐍 **ʟᴀɴɢᴜᴀɢᴇ :** Python 3.10+\n"
        "🛰️ **ғʀᴀᴍᴇᴡᴏʀᴋ :** Kurigram (Pyrogram) + Telethon\n"
        "☁️ **ʜᴏsᴛɪɴɢ :** Koyeb Cloud (Frankfurt, FRA)\n"
        "🔒 **sᴇᴄᴜʀɪᴛʏ :** Pure in-memory authorization\n"
        f"👑 **ᴅᴇᴠᴇʟᴏᴩᴇʀ :** [ᴛʜᴇ ᴠɪᴘ ʙᴏʏ](tg://user?id={OWNER_ID})\n"
        "────────────────────────\n"
        "❤️ *Thank you for using our services!*"
    )


@Client.on_message(filters.private & filters.incoming & filters.command("start"))
async def start(bot: Client, msg: Message):
    me2 = bot.me.mention if getattr(bot, "me", None) else (await bot.get_me()).mention
    text = get_start_text(msg.from_user.mention, me2)
    await bot.send_message(
        chat_id=msg.chat.id,
        text=text,
        reply_markup=START_MARKUP,
        disable_web_page_preview=True,
    )


@Client.on_message(filters.private & filters.incoming & filters.command("help"))
async def help_cmd(bot: Client, msg: Message):
    await msg.reply_text(get_help_text(), reply_markup=HELP_MARKUP)


@Client.on_message(filters.private & filters.incoming & filters.command("about"))
async def about_cmd(bot: Client, msg: Message):
    await msg.reply_text(get_about_text(), reply_markup=ABOUT_MARKUP)
