import traceback
import sys
import os
import re
import subprocess
from io import StringIO, BytesIO
from kanaorobot import KANAO, ALLOWED_USERS
from kanaorobot.sql import chats_db
from pyrogram import filters

from kanaorobot.utils.errors import capture_err


async def aexec(code, client, message):
    exec(
        f'async def __aexec(client, message): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return await locals()['__aexec'](client, message)


@KANAO.on_message(filters.user(ALLOWED_USERS) & filters.command("eval"))
@capture_err
async def evaluate(client, message):
    status_message = await message.reply_text("`Running ...`")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        await status_message.delete()
        return
    reply_to_id = message.message_id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = f"<b>OUTPUT</b>:\n<code>{evaluation.strip()}</code>"
    if len(final_output) > 4096:
        filename = 'output.txt'
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(final_output))
        await message.reply_document(
            document=filename,
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id
        )
        os.remove(filename)
        await status_message.delete()
    else:
        await status_message.edit(final_output)



@KANAO.on_message(filters.user(ALLOWED_USERS) & filters.command("term"))
@capture_err
async def terminal(client, message):
    if len(message.text.split()) == 1:
        await message.reply("Usage: `/term echo owo`")
        return
    args = message.text.split(None, 1)
    teks = args[1]
    if "\n" in teks:
        code = teks.split("\n")
        output = ""
        for x in code:
            shell = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', x)
            try:
                process = subprocess.Popen(
                    shell,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            except Exception as err:
                print(err)
                await message.reply("""
**Error:**
```{}```
""".format(err))
            output += "**{}**\n".format(code)
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', teks)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(etype=exc_type, value=exc_obj, tb=exc_tb)
            await message.reply("""**Error:**\n```{}```""".format("".join(errors)))
            return
        output = process.stdout.read()[:-1].decode("utf-8")
    if str(output) == "\n":
        output = None
    if output:
        if len(output) > 4096:
            with open("thebot/output.txt", "w+") as file:
                file.write(output)
            await client.send_document(message.chat.id, "thebot/output.txt", reply_to_message_id=message.message_id,
                                    caption="`Output file`")
            os.remove("thebot/output.txt")
            return
        await message.reply(f"**Output:**\n```{output}```", parse_mode='markdown')
    else:
        await message.reply("**Output:**\n`No Output`")


@KANAO.on_message(filters.user(ALLOWED_USERS) & filters.command("stats", prefixes='/'))
async def stats_text(_, message):
    stats = "──「 <b>Current stats</b> 」──\n"
    stats += f"-> <code>{chats_db.num_users()}</code> users, across <code>{chats_db.num_chats()}</code> chats"
    await message.reply(stats)


@KANAO.on_message(~filters.me & filters.user(ALLOWED_USERS) & filters.command("chats", prefixes='/'))
async def chat_stats(client, message):
    all_chats = chats_db.get_all_chats() or []
    chatfile = 'List of chats.\n0. Chat name | Chat ID | Members count\n'
    P = 1
    for chat in all_chats:
        curr_chat = await client.get_chat(chat.chat_id)
        bot_member = await curr_chat.get_member(5675469187)
        chat_members = await client.get_chat_members_count(chat.chat_id)
        chatfile += "{}. {} | {} | {}\n".format(P, chat.chat_name,
                                                    chat.chat_id, chat_members)
        P += 1

    with BytesIO(str.encode(chatfile)) as output:
        output.name = "chatlist.txt"
        await message.reply_document(
            document=output,
            caption="Here is the list of chats in my database.")


@KANAO.on_message(filters.all & filters.group)
def log_user(client, message):
    chat = message.chat
    chats_db.update_user(message.from_user.id, message.from_user.username, chat.id,
                    chat.title)

    if message.reply_to_message:
        chats_db.update_user(message.reply_to_message.from_user.id,
                        message.reply_to_message.from_user.username, chat.id,
                        chat.title)

    if message.forward_from:
        chats_db.update_user(message.forward_from.id, message.forward_from.username)
