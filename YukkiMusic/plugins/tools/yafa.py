# Dev : https://t me/YY8GG
#Group : https://t.me/YaFaGr
import requests
from strings.filters import command
from gpytranslate import Translator
from aiohttp import ClientSession
from pyrogram import filters, Client
import re
from config import (YAFA_NAME, YAFA_CHANNEL, SUDO_USER,
                    START_IMG_URL, BOT_USERNAME)
from pyrogram.types import (InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)
from telegraph import upload_file
from traceback import format_exc
from YukkiMusic import app
from typing import Union

@app.on_message(command(["ترجمة","/tr"]))
async def tr(_, message):
    trl = Translator()
    if message.reply_to_message and (message.reply_to_message.text or message.reply_to_message.caption):
        if len(message.text.split()) == 1:
            target_lang = "ar"
        else:
            target_lang = message.text.split()[1]
        if message.reply_to_message.text:
            text = message.reply_to_message.text
        else:
            text = message.reply_to_message.caption
    else:
        if len(message.text.split()) <= 2:
            return await message.reply_text("أرسل الامر على هذا الشكل :\n[Available options](https://telegra.ph/Lang-Codes-02-22).\n<b>Usage:</b> <code>/tr ar</code>",disable_web_page_preview=True)
        target_lang = message.text.split(None, 2)[1]
        text = message.text.split(None, 2)[2]
    detectlang = await trl.detect(text)
    try:
        data = requests.get(f"https://api.safone.tech/translate?text={text}&target={target_lang}").json()
        tekstr = await trl(text, targetlang=target_lang)
    except ValueError as err:
        return await message.reply_text(f"Error: <code>{str(err)}</code>")
    return await message.reply_text(f"<b>Translated:</b> from {data['origin']} to {data['target']} \n<code>{data['translated']}</code>")

def ReplyCheck(message: Message):
    reply_id = None
    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id
    elif not message.from_user.is_self:
        reply_id = message.message_id
    return reply_id


session = ClientSession()
pattern = re.compile(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$")
BASE = "https://batbin.me/"

async def post(url: str, *args, **kwargs):
    async with session.post(url, *args, **kwargs) as resp:
        try:
            data = await resp.json()
        except Exception:
            data = await resp.text()
    return data

async def paste(content: str):
    resp = await post(f"{BASE}api/v2/paste", data=content)
    if not resp["success"]:
        return
    return BASE + resp["message"]


@app.on_message(command(["طباعة","/pr"]))
async def paste_func(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("الرد على رسالة ب  `/pr`")
    r = message.reply_to_message
    if not r.text and not r.document:
        return await message.reply_text("يتم دعم النصوص والمستندات فقط ")
    m = await message.reply_text("لصق ...")
    if r.text:
        content = str(r.text)
    elif r.document:
        if r.document.file_size > 40000:
            return await m.edit("يمكنك فقط لصق ملفات أصغر من 40 كيلوبايت .")
        if not pattern.search(r.document.mime_type):
            return await m.edit("يمكن لصق الملفات النصية فقط .")
        doc = await message.reply_to_message.download()
        async with aiofiles.open(doc, mode="r") as f:
            content = await f.read()
        os.remove(doc)
    link = await paste(content)
    kb = [[InlineKeyboardButton(text="رابط اللصق", url=link)]]
    try:
        if m.from_user.is_bot:
            await message.reply_photo(photo=link,quote=False,caption="تم نسخ النص",reply_markup=InlineKeyboardMarkup(kb),)
        else:
            await message.reply_photo(photo=link,quote=False,caption="تم نسخ النص",reply_markup=InlineKeyboardMarkup(kb),)
        await m.delete()
    except Exception:
        await m.edit("فتح الرابط", reply_markup=InlineKeyboardMarkup(kb))


@app.on_message(command(["ميديا", "/tm", "tgm"]))
async def telegraph(client, message):
    replied = message.reply_to_message
    if not replied:
        return await message.reply("الرد على ملف وسائط مدعوم ")
    if not (
        (replied.photo and replied.photo.file_size <= 5242880)
        or (replied.animation and replied.animation.file_size <= 5242880)
        or (replied.video and replied.video.file_name.endswith(".mp4") and replied.video.file_size <= 5242880)
        or (replied.document and replied.document.file_name.endswith((".jpg", ".jpeg", ".png", ".gif", ".mp4")) and replied.document.file_size <= 5242880)):
        return await message.reply("غير مدعوم !")
    download_location = await client.download_media(message=message.reply_to_message,file_name="root/downloads/")
    try:
        response = upload_file(download_location)
    except Exception as document:
        await message.reply(message, text=document)
    else:
        button_s = InlineKeyboardMarkup([[InlineKeyboardButton("فتح الرابط 🔗", url=f"https://telegra.ph{response[0]}")]])
        await message.reply(f"**الرابط »**\n`https://telegra.ph{response[0]}`",disable_web_page_preview=True,reply_markup=button_s)
    finally:
        os.remove(download_location)


@app.on_message(command(["الرابط","/link"]) & ~filters.bot & ~filters.private)
async def invitelink(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        return await message.reply_text("قم برفعي مسؤول في المجموعة أولا ؟")
    await message.reply_text(f"**تم إنشاء رابط الدعوة بنجاح :**\n {invitelink}")

    
@app.on_message(command(["قول"])
    & filters.group
    & ~filters.edited
)
def echo(client, msg):
    text = msg.text.split(None, 1)[1]
    msg.reply(text)
    
    
@app.on_message(command(["الاوامر"])
    & filters.group
    & ~filters.edited
)
async def khalid(client: Client, message: Message):
    usr = await client.get_users(message.from_user.id)
    name = usr.first_name
    async for photo in client.iter_profile_photos(message.from_user.id, limit=1):
                    await message.reply_text( 
                    f"""- شغل أو تشغيل : لبدء تشغيل الاغاني.

- بنك أو بنغ : لقياس سرعة نت البوت.

- تخطي : لتخطي الأغنية الحالية.

- كتم أو اسكت : لكتم الأغنية صوت الأغنية.

- كمل : لفك كتم صوت الأغنية.

- تحميل أو بحث : لتحميل أغنية او فيديو من اليوتيوب

- انهاء : لأنهاء بث الاغنية.

طباعة : بالرد على نص انلجيزي لطباعته بصورة.

- ترجمة : بالرد على نص او كتابة نص مثال :
ترجمة en او ترجمة ar + النص.

- الرابط : لجلب رابط المجموعة.

- ميديا : لاستخراج رابط صورة او متحركة او ملصق.

- ايدي : لجلب ايديك وايدي المجموعة.

- قول + الكلام.""",
        reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(f"• {YAFA_NAME} •", url=f"{YAFA_CHANNEL}"),
                ],[
                InlineKeyboardButton("• أضفني الى مجموعتك •", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
                ]
            ]
        ),
    )
    
@app.on_message(command(["سورس","السورس","المطور","المبرمج"])
    & filters.group
    & ~filters.edited
)
async def khalid(client: Client, message: Message):
    await message.reply_photo(
        photo=f"{START_IMG_URL}",
        caption=f"""• Welcome to the Music Source 🎗.""",
        reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("• المطور •", url=f"{SUDO_USER}",
                ),
                InlineKeyboardButton(f"• السورس •", url=f"{YAFA_CHANNEL}",
                ),
            ],
            [
                InlineKeyboardButton("• أضفني الى مجموعتك •", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
                ]
            ]
        ),
    )
