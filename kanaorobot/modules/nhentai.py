import requests

from pyrogram import filters
from pyrogram.types import (InlineKeyboardMarkup,
                            InlineKeyboardButton,
                            InlineQueryResultArticle,
                            InputTextMessageContent
                            )

from kanaorobot import KANAO, telegraph

from kanaorobot.utils.errors import capture_err


@KANAO.on_message(~filters.me & filters.command('nhentai', prefixes='/'), group=8)
@capture_err
async def nhentai(client, message):
    query = message.text.split(" ")[1]
    title, tags, artist, total_pages, post_url, cover_image = nhentai_data(query)
    await message.reply_text(
        f"<code>{title}</code>\n\n<b>Tags:</b>\n{tags}\n<b>Artists:</b>\n{artist}\n<b>Pages:</b>\n{total_pages}",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Read Here",
                        url=post_url
                    )
                ]
            ]
        )
    )

@KANAO.on_inline_query(filters.regex(r'^nhentai (\d+)$'))
@capture_err
async def inline_nhentai(client, inline_query):
    query = int(inline_query.matches[0].group(1))
    n_title, tags, artist, total_pages, post_url, cover_image = nhentai_data(query)
    reply_message = f"<code>{n_title}</code>\n\n<b>Tags:</b>\n{tags}\n<b>Artists:</b>\n{artist}\n<b>Pages:</b>\n{total_pages}"
    await inline_query.answer( 
        results=[
                InlineQueryResultArticle(
                        title=n_title,
                        input_message_content=InputTextMessageContent(
                            reply_message
                        ),
                        description=tags,
                        thumb_url=cover_image,
                        reply_markup=InlineKeyboardMarkup(
                            [[
                            InlineKeyboardButton(
                                "Read Here",
                                url=post_url
                                )
                            ]]
                        )
                    )
                ],
                cache_time=1
            )


def nhentai_data(noombers):
    url = f"https://nhentai.net/api/gallery/{noombers}"
    res = requests.get(url).json()
    pages = res["images"]["pages"]
    info = res["tags"]
    title = res["title"]["english"]
    links = []
    tags = ""
    artist = ''
    total_pages = res['num_pages']
    extensions = {
        'j':'jpg',
        'p':'png',
        'g':'gif'
    }
    for i, x in enumerate(pages):
        media_id = res["media_id"]
        temp = x['t']
        file = f"{i+1}.{extensions[temp]}"
        link = f"https://i.nhentai.net/galleries/{media_id}/{file}"
        links.append(link)

    for i in info:
        if i["type"]=="tag":
            tag = i['name']
            tag = tag.split(" ")
            tag = "_".join(tag)
            tags+=f"#{tag} "
        if i["type"]=="artist":
            artist=f"{i['name']} "

    post_content = "".join(f"<img src={link}><br>" for link in links)

    post = telegraph.create_page(
        f"{title}",
        html_content=post_content,
        author_name="@Kanaorobot", 
        author_url="https://t.me/kanaoroBot"
    )
    return title,tags,artist,total_pages,post['url'],links[0]


async def _download(_id, dl_path, outfile_path):
    title, num_pages, artist, lang, tags, page_links = await nhentai_data(_id)
    imgs = []
    for i in range(1, int(num_pages) + 1):
        wget.download(page_links[i - 1], dl_path)
        suffix = page_links[i - 1].split(".")[-1]
        fname = f"{dl_path}//{i}.{suffix}"
        img = Image.open(fname)
        if img.mode == "RGBA":
            img = img.convert("RGB")
        imgs.append(img)
    
    imgs[0].save(outfile_path, save_all = True, quality = 100, append_images = imgs[1:])

                    
