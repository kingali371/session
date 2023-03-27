from pyrogram.types import Message
from telethon import TelegramClient
from pyrogram import Client, filters
from pyrogram1 import Client as Client1
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from pyrogram1.errors import (
    ApiIdInvalid as ApiIdInvalid1,
    PhoneNumberInvalid as PhoneNumberInvalid1,
    PhoneCodeInvalid as PhoneCodeInvalid1,
    PhoneCodeExpired as PhoneCodeExpired1,
    SessionPasswordNeeded as SessionPasswordNeeded1,
    PasswordHashInvalid as PasswordHashInvalid1
)
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

import config



ask_ques = "**» • ذا كنـت تـريد تنـصيـب سـورس مـيوزك فـأختـار بـايـروجـرام\n• واذا تـريـد تنـصـيب التليثون فـأخـتار تيرمكـس\n• اذا كنـت سـورسـك مـتحـدث مـع اخـر تحديثات الـباروجـرام فا اخـتار بـايـروجـرام [New] \n• يوحد استخرجات جـلسـات لـي البـوتات :**"
buttons_ques = [
    [
        InlineKeyboardButton("🎙 بـايـࢪوجـࢪام 🎙", callback_data="pyrogram1"),
        InlineKeyboardButton("🎙 بـايـࢪوجـࢪام ᴠ2🎙", callback_data="pyrogram"),
    ],
    [
        InlineKeyboardButton("🎛 تـلـيـثـونـ 🎛", callback_data="telethon"),
    ],
    [
        InlineKeyboardButton("📟  بـايـࢪوجـࢪام بـوتـ  📟", callback_data="pyrogram_bot"),
        InlineKeyboardButton("🕹 تـلـيـثـونـ بـوتـ 🕹", callback_data="telethon_bot"),
    ],
]

gen_button = [
    [
        InlineKeyboardButton(text="🌐 ⍆ اضغط لبدا استخراج كود ⍅🌐", callback_data="generate")
    ]
]




@Client.on_message(filters.private & ~filters.forwarded & filters.command(["generate", "gen", "string", "str"]))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(bot: Client, msg: Message, telethon=False, old_pyro: bool = False, is_bot: bool = False):
    if telethon:
        ty = "ᴛᴇʟᴇᴛʜᴏɴ"
    else:
        ty = "ᴩʏʀᴏɢʀᴀᴍ"
        if not old_pyro:
            ty += " ᴠ2"
    if is_bot:
        ty += " ʙᴏᴛ"
    await msg.reply(f"» » ⚡ ¦ بـدء إنـشـاء جـلسـة **{ty}** ...")
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, "🎮حسنـا قم بأرسال الـ API_ID\n\nاضغط /skip عشان تكمل بالموجدين.", filters=filters.text)
    if await cancelled(api_id_msg):
        return
    if api_id_msg.text == "/skip":
        api_id = config.API_ID
        api_hash = config.API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
        except ValueError:
            await api_id_msg.reply("**ᴀᴩɪ_ɪᴅ** ᴍᴜsᴛ ʙᴇ ᴀɴ ɪɴᴛᴇɢᴇʀ, sᴛᴀʀᴛ ɢᴇɴᴇʀᴀᴛɪɴɢ ʏᴏᴜʀ sᴇssɪᴏɴ ᴀɢᴀɪɴ.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        api_hash_msg = await bot.ask(user_id, "» » 🎮حسنـا قم بأرسال الـ API_HASH", filters=filters.text)
        if await cancelled(api_hash_msg):
            return
        api_hash = api_hash_msg.text
    if not is_bot:
        t = "» » ✔️الان ارسل رقمك مع رمز دولتك , مثال :+201205361728"
    else:
        t = "ᴩʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ **ʙᴏᴛ_ᴛᴏᴋᴇɴ** ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.\nᴇxᴀᴍᴩʟᴇ : `5432198765:abcdanonymousterabaaplol`'"
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply("»⬇️انتـظر لـحظـه سـوف نـرسـل كـود لحسابـك بالتليجـرام.")
    else:
        await msg.reply("» ᴛʀʏɪɴɢ ᴛᴏ ʟᴏɢɪɴ ᴠɪᴀ ʙᴏᴛ ᴛᴏᴋᴇɴ...")
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    elif old_pyro:
        client = Client1(":memory:", api_id=api_id, api_hash=api_hash)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError, ApiIdInvalid1):
        await msg.reply("» يقلب **ᴀᴩɪ_ɪᴅ** و **ᴀᴩɪ_ʜᴀsʜ** بتوع اك محذوف. \n\nاعمل استرت يقلب عشن تبدا من الاول.", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError, PhoneNumberInvalid1):
        await msg.reply("» يقلب **الرقم** مش معمول بيه اكونت اصلا علي التلي.\n\nاعمل استرت وابدا من الاول وابعت الرقم متخفش.", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await bot.ask(user_id, "»»[شـوف آلصـورهہ‏‏ الكود مبعوت ازاي وابعت زيه عشان ميجيش ليك.ابطاء](https://telegra.ph/file/da1af082c6b754959ab47.jpg)» 🔍من فضلك افحص حسابك بالتليجرام وتفقد الكود من حساب اشعارات التليجرام. إذا كان\n  هناك تحقق بخطوتين( المرور ) ، أرسل كلمة المرور هنا بعد ارسال كود الدخول بالتنسيق أدناه.- اذا كانت كلمة المرور او الكود  هي\n 12345 يرجى ارسالها بالشكل التالي 1 2 3 4 5 مع وجود مسـافـات بين الارقام اذا احتجت مساعدة @T_3_A..", filters=filters.text, timeout=600)
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply("» لقد تخطـيـﮯت آلحد آلقصـيـﮯ 10 دقآيـﮯق\n\nآعمـل آسـترت عشـآن تسـتخرج مـن آلآول", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError, PhoneCodeInvalid1):
            await msg.reply("» آلگود آل بعتهہ‏‏ غلطـ **رگز يـﮯقلب.**\n\nآعمـل آسـترت عشـآن تسـتخرج جلسـهہ‏‏ مـ آلآول.", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError, PhoneCodeExpired1):
            await msg.reply("» آلگود مـنهہ‏‏يـﮯ **مدته انتهت.**\n\nآعمـل آسـترت عشـآن تسـتخرج جلسـهہ‏‏ مـ آلآول", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError, SessionPasswordNeeded1):
            try:
                two_step_msg = await bot.ask(user_id, "» آبعت **رمـز آلتحقق** بآسـورد آلآگ عشـآن .", filters=filters.text, timeout=300)
            except TimeoutError:
                await msg.reply("» فآت 5 دقآيـﮯق.\n\nآنتهہ‏‏ت آلمـدهہ‏‏ آعمـل آسـترت وآبدآ مـ .", reply_markup=InlineKeyboardMarkup(gen_button))
                return
            try:
                password = two_step_msg.text
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
                if await cancelled(api_id_msg):
                    return
            except (PasswordHashInvalid, PasswordHashInvalidError, PasswordHashInvalid1):
                await two_step_msg.reply("» آلبآسـورد غلطـ يـﮯقلب\n\nآعمـل آسـترت وجرب تآنيـﮯ وآتآگد مـ ", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
                return
    else:
        if telethon:
            await client.start(bot_token=phone_number)
        else:
            await client.sign_in_bot(phone_number)
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = f"جلستك يبروو {ty} sᴛʀɪɴɢ sᴇssɪᴏɴ** \n\n`{string_session}` \n\n**ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ :** @T_3_A \n🍒 **ɴᴏᴛᴇ :** حافظ عليها ممكن حد يخترقكك بيها\n اشترك بالحب @L_H_V 🥺"
    try:
        if not is_bot:
            await client.send_message("me", text)
        else:
            await bot.send_message(msg.chat.id, text)
    except KeyError:
        pass
    await client.disconnect()
    await bot.send_message(msg.chat.id, "» » ✅تم استخراج الجلسه بنجاح ️ {} .\n\n🔍من فضلك تفحص الرسايل المحفوظه بحسابك!  ! \n\n**𝙳𝙴𝚅 𝙾𝙼𝙰𝚁𐇗** @T_3_A 🥺".format("ᴛᴇʟᴇᴛʜᴏɴ" if telethon else "ᴩʏʀᴏɢʀᴀᴍ"))


async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("**» تم انهاء آلعمـليـﮯهہ‏‏**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("**» تمـ آعآد‏‏هہ تشـغيـﮯل آلبوت !**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif "/skip" in msg.text:
        return False
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("**» تمـ آنهہ‏‏آء آلعمـليـﮯهہ‏‏!**", quote=True)
        return True
    else:
        return False
