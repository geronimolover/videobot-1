from datetime import datetime
from time import time

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from config import BOT_USERNAME
from helpers.decorators import sudo_users_only
from helpers.filters import command

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_message(command(["start", f"start@{BOT_USERNAME}"]))
async def start(_, m: Message):
    if m.chat.type == "private":
        await m.reply_text(
            f"✨ **Hello there, I am a telegram group video streaming bot.**\n\n💭 **I was created to @song_requestgroup "
            f"**\n\n **I can Also find lyrics of any song** 👇🏻",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                        "➕You cant add me to your Group ➕", url=f"https://t.me/the_song_request_bot")
                ], [
                    InlineKeyboardButton(
                        "📚 HOW TO USE THIS BOT", callback_data="cbguide")
                ], [
                    InlineKeyboardButton(
                        "🌐 Movie Group", url="https://t.me/all_super_movies")
                ], [
                    InlineKeyboardButton(
                        "💬 Group", url="https://t.me/song_requestgroup"),
                    InlineKeyboardButton(
                        "📣 Channel", url="https://t.me/free_music123")
                ], [
                    InlineKeyboardButton(
                        "👩🏻‍💻 Developer", url="https://t.me/geronimo1234")
                ], [
                    InlineKeyboardButton(
                        "❔ Report your problems", url="https://t.me/musicgroupbugbot")
                ]]
            ))
    else:
        await m.reply_text("**✨ bot is online now ✨**",
                           reply_markup=InlineKeyboardMarkup(
                               [[
                                   InlineKeyboardButton(
                                       "❔ HOW TO USE THIS BOT", callback_data="cbguide")
                               ], [
                                   InlineKeyboardButton(
                                       "🌐 Search Youtube", switch_inline_query='')
                               ], [
                                   InlineKeyboardButton(
                                       "📚 Command List", callback_data="cblist")
                               ]]
                           )
                           )


@Client.on_message(command(["alive", f"alive@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def alive(_, m: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m.reply_text(
        f"""✅ **bot is running**\n<b>💠 **uptime:**</b> `{uptime}`""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✨ Group", url=f"https://t.me/song_requestgroup"
                    ),
                    InlineKeyboardButton(
                        "📣 Channel", url=f"https://t.me/free_music123"
                    )
                ]
            ]
        )
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(_, m: Message):
    sturt = time()
    m_reply = await m.reply_text("pinging...")
    delta_ping = time() - sturt
    await m_reply.edit_text(
        "🏓 `PONG!!`\n"
        f"⚡️ `{delta_ping * 1000:.3f} ms`"
    )


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
@sudo_users_only
async def get_uptime(_, m: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m.reply_text(
        "🤖 bot status 🤖\n\n"
        f"• **uptime:** `{uptime}`\n"
        f"• **start time:** `{START_TIME_ISO}`"
    )
