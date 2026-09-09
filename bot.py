import time
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

# بياناتك الخاصة مدرجة هنا بالكامل وجاهزة
API_ID = 35910181
API_HASH = "b49c71b84883853e18b5b88aacf5bc5b"
BOT_TOKEN = "8911215544:AAHLhk8Rc5ns1V4OvVAVoDYrBuGO85lLXkk"

app = Client("mention_bot_app", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

logging.basicConfig(level=logging.INFO)

@app.on_message(filters.command("all", prefixes=["@"]) & filters.group)
async def mention_all_handler(client: Client, message: Message):
    chat_id = message.chat.id
    
    # استخراج النص المرفق مع الأمر
    text_parts = message.text.split(maxsplit=1)
    custom_text = text_parts[1] if len(text_parts) > 1 else "تنبيه للجميع!"

    try:
        await message.delete()
    except Exception:
        pass

    # جمع كل أعضاء الكروب بلا استثناء
    users = []
    try:
        async for member in client.get_chat_members(chat_id):
            if member.user.is_bot or member.user.is_deleted:
                continue
            users.append(member.user)
    except Exception as e:
        logging.error(f"خطأ في سحب الأعضاء: {e}")
        await message.reply("ما أگدر أسحب الأعضاء، تأكد أن البوت مشرف ولديه صلاحيات كاملة بالكروب!")
        return

    if not users:
        await message.reply("ماكو أعضاء بالكروب!")
        return

    # تقسيم الأعضاء إلى دفعات (كل دفعة 10 أشخاص مثل ما طلبت)
    chunk_size = 10
    for i in range(0, len(users), chunk_size):
        chunk = users[i:i + chunk_size]
        
        mentions = []
        for user in chunk:
            name = user.first_name or "صديقي"
            mentions.append(f"[{name}](tg://user?id={user.id})")
        
        final_message = f"{custom_text}\n\n" + " ".join(mentions)
        
        try:
            await client.send_message(chat_id, final_message)
        except FloodWait as e:
            logging.warning(f"انتظار مؤقت لمدة {e.value} ثانية لتجنب الحظر...")
            time.sleep(e.value)
            await client.send_message(chat_id, final_message)
        except Exception as e:
            logging.error(f"خطأ أثناء إرسال الدفعة: {e}")
            continue

if __name__ == '__main__':
    print("البوت يعمل الآن وجاهز للمنشن...")
    app.run()
