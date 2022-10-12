#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import speedtest
from pyrogram import filters
from strings import get_command
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS

# Commands
SPEEDTEST_COMMAND = get_command("SPEEDTEST_COMMAND")


def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit("تحميل السرعة...")
        test.download()
        m = m.edit("تشغيل اختبار سرعة التحميل...")
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit("جار مشاركة النتائج...")
    except Exception as e:
        return m.edit(e)
    return result


@app.on_message(filters.command(SPEEDTEST_COMMAND) & SUDOERS)
async def speedtest_function(client, message):
    m = await message.reply_text("اختبار سرعة التشغيل")
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m)
    output = f"""**نتائج سرعة النت**
    
<u>**العميل:**</u>
**__مزود خدمة الإنترنت :__** {result['client']['isp']}
**__دولة :__** {result['client']['country']}
  
<u>**الخادم :**</u>
**__اسم :__** {result['server']['name']}
**__دولة :__** {result['server']['country']}, {result['server']['cc']}
**__كفيل :__** {result['server']['sponsor']}
**__وقت الإستجابة :__** {result['server']['latency']}  
**__بينغ :__** {result['ping']}"""
    msg = await app.send_photo(
        chat_id=message.chat.id, 
        photo=result["share"], 
        caption=output
    )
    await m.delete()
