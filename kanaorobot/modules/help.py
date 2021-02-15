import asyncio
from kanaorobot import KANAO
from pyrogram import filters
from .callback import callback_data
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from kanaorobot.utils.errors import capture_err

buttons = [
    [
        InlineKeyboardButton('Anime', switch_inline_query_current_chat='anime '),
        InlineKeyboardButton('Manga', switch_inline_query_current_chat='manga '),
        InlineKeyboardButton('nHentai', switch_inline_query_current_chat='nhentai ')
    ],
    [
        InlineKeyboardButton('Airing', switch_inline_query_current_chat='airing '),
        InlineKeyboardButton('Character', switch_inline_query_current_chat='char '),
    ]
]

@KANAO.on_callback_query(callback_data(['help']))
@capture_err
async def chelp(_, client):
    await client.edit_message_text(
        'Available cmds for now :\n /animeinfo - search anime on AniList\n /mangainfo - search manga on Anilist\n /charinfo - search character on Anilist\n /airinfo - check airing status of an anime\n /nhentai ID - returns the nhentai in telegraph instant preview format.\n /schedule - Find Anime Schedule',
          reply_markup=InlineKeyboardMarkup(buttons)
    )

INFO_TEXT = """
Made with ❤️ by @anime_spotfloix
"""

@KANAO.on_message(~filters.me & filters.command('help', prefixes='/'), group=8)
@capture_err
async def help(_, message):
    buttons = [
        [
            InlineKeyboardButton('Anime', switch_inline_query_current_chat='anime '),
            InlineKeyboardButton('Manga', switch_inline_query_current_chat='manga '),
            InlineKeyboardButton('nHentai', switch_inline_query_current_chat='nhentai ')
        ],
        [
            InlineKeyboardButton('Airing', switch_inline_query_current_chat='airing '),
            InlineKeyboardButton('Character', switch_inline_query_current_chat='char '),
        ]
    ]
    if message.chat.type == "private":
       await message.reply_text(
        'Available cmds for now :\n /animeinfo - search anime on AniList\n /mangainfo - search manga on Anilist\n /charinfo - search character on Anilist\n /airinfo - check airing status of an anime\n /nhentai ID - returns the nhentai in telegraph instant preview format.\n /schedule - Find Anime Schedule',
        reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Help",
                url=f"t.me/kanaorobot?start=help")]])
        await message.reply("Click the button below.",
                            reply_markup=buttons)


@KANAO.on_message(filters.command(["about"], prefixes = "/") & ~filters.edited)
async def info(client, message):
    buttons = [
                [InlineKeyboardButton("⭐ Me?", url = "https://github.com/animespotflix/kanaobot"), InlineKeyboardButton("Report Issues", url = "https://t.me/@Cap_tainlevi")]
              ]
    await KANAO.send_message(chat_id = message.chat.id, text = INFO_TEXT, reply_markup = InlineKeyboardMarkup(buttons))
