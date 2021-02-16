from kanaorobot import KANAO
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from kanaorobot.utils.errors import capture_err


@KANAO.on_message(~filters.me & filters.command('start', prefixes='/'), group=8)
@capture_err
async def start(_, message):
   if message.chat.type == "private":
     if len(message.text.split()) >= 2:
       suckz = message.text.split()[1]
       if suckz == "help":
          buttons = [
                     [
                        InlineKeyboardButton('Anime', switch_inline_query_current_chat='anime '),
                        InlineKeyboardButton('Manga', switch_inline_query_current_chat='manga '),
                        InlineKeyboardButton('nHentai', switch_inline_query_current_chat='nhentai ')
                     ],
                     [
                        InlineKeyboardButton('Airing', switch_inline_query_current_chat='airing '),
                        InlineKeyboardButton('Character', switch_inline_query_current_chat='char ')
                     ]
                  ]
          await message.reply_text(' Available cmds for now :\n /anime - search anime on AniList\n /malanime - search anime on Myanimelist\n /manga - search manga on Anilist\n /malmanga - search manga on myanimelist\n /character - search character on Anilist\n /malcharacter - search character on myanimelist\n /airing - check airing status of an anime\n /nhentai ID - returns the nhentai in telegraph instant preview format.\n /schedule - Find Anime Schedule', reply_markup=InlineKeyboardMarkup(buttons))
     else:
       photo = "https://cdn.discordapp.com/attachments/741622639000551474/810791708622454814/400125700350_244266.jpg"
       buttons = [
            [
            InlineKeyboardButton('Anime', switch_inline_query_current_chat='anime '),
            InlineKeyboardButton('Manga', switch_inline_query_current_chat='manga '),
            InlineKeyboardButton('nHentai', switch_inline_query_current_chat='nhentai ')
            ],
            [
            InlineKeyboardButton('Airing', switch_inline_query_current_chat='airing '),
            InlineKeyboardButton('Character', switch_inline_query_current_chat='char ')
            ],
            [
            InlineKeyboardButton('Help', 'help'),
            ]
                  ]
       await message.reply_photo(photo,
         caption='Hi, I Am Kanao\nI can help you to find everything about anime\nYou can use command or inline to using me 😆',
         reply_markup=InlineKeyboardMarkup(buttons))
   else:
       await message.reply_text("Hi there, I'm Kanao.")
