import asyncio
import os
import time
from telethon import TelegramClient, errors
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.errors import MessageIdInvalidError
from telethon.tl.types import Updates, UpdateNewMessage, UpdateNewChannelMessage
from flask import Flask
from threading import Thread
import random
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os
import nest_asyncio
import asyncio
from datetime import datetime
from telethon.tl.types import Channel

# بقیه ایمپورت‌های خودت مثل telethon و asyncio و ...

app = Flask('')

@app.route('/')
def home():
    return "✅ Bot is running."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 🧠 اینو قبل از اجرای اصلی برنامه صدا بزن:
keep_alive()

# تنظیمات اصلی
api_id = 27950812  # API ID شما
api_hash = '144c28cddc91020362d77a3197f454ce'  # API Hash شما
phone_number = '+989920189121'
SESSION_FILE = 'session.txt'
LINKS_FILE = 'links.txt'
UNABLE_FILE = 'unable.txt'
MAX_TRIES = 3  # تعداد تلاش‌های مجاز
WAIT_TIME = 5  # مدت زمان انتظار بین هر تلاش (به ثانیه)

messages_list = [
    "حوصلم سر رفتهههه. وای پوکیدیم",
    "سایت تقویم شمسی معتبر کسی میشناسه؟",
    "اینجا گروه چیه میشه بگین؟",
    "کیا اینجا ماهواره دارن؟ شبکه ها رو نشون میده؟",
    "وای چقدر هوا گرم شده. رسما تابستونه",
    "لینک گروه چت کسی داره بفرسته؟",
    "کسی اینجا موهای بدنشو لیزر کرده؟ میشه راهنمایی کنین؟",
    "بازی باحال چی سراغ دارین؟ ترجیحا آنلاین باشه",
    "خیس شدیم تو این گرما. آب و هوا چرا اینجوریه؟",
    " نمی‌دونم خسته‌م یا فقط بی‌حوصله ",
    "بچه ها بنظتون قلیون چی بگیرم خوبه؟",
    " اون آهنگه رو که میگه یچی بده دود کنم یادم برن آدما رو کسی داره؟ ",
    " دلم برای یه روز بی‌دغدغه تنگ شده. یه روز معمولی 🫠 ",
    " آدم‌ها خیلی وقتا حرف نمی‌زنن چون می‌دونن شنیده نمیشن ",
    " بارون چی میگه؟ 😐 ",
    " دیشب تصادفی یه آهنگ شنیدم، پرت شدم گذشته ",
    " همه‌مون دنبال یه چیزیم، ولی کسی دقیق نمی‌دونه چیه ",
    " آروم بودن خیلی فرق داره با تنها بودن، قبول دارین؟ ",
    "کی پایس امشب بریم بیرون؟",
    " هواش یه جوریه که انگار باید یه نامه قدیمی پیدا کنی بخونی ",
    " نه انگیزه دارم، نه انرژی، نه هدف",
    "امان از روابط پرخطر",
    " بعضی صداها فقط یادآور یه نفرن ",
    " بعضیا فقط میان که برن، بعضیا هم میان که بمونن ولی تهش بازم میرن ",
    " تازه فهمیدم مرتضی پاشایی ترک جدید داده، خیلی خوبه ",
    " هواش دقیقا اونیه که آدم می‌خواد زل بزنه به پنجره ",
    " مغزم پره ولی هیچ فکری هم نیست. حوصلم ترکید ",
    " کاش می‌شد یه بار دیگه اون موقع‌ها رو زندگی کرد ",
    " کسی آهنگ خوب داره بفرسته؟ دلم یه چیز خاص می‌خواد ",
    " دلم می‌خواد فقط یه مدت خاموش باشم ",
    " این اخبار روز به روز عجیب‌تر میشه ",
    " گاهی لازمه فقط یه مدت از همه چی فاصله بگیری ",
    " شب که میشه، فکرا یه جور دیگه میان سراغت ",
    " کاش یکی بود بگه چی قراره بشه تهش ",
    " امروز عجیباً دلم قهوه خواست، اونم تلخ تلخ ",
    " جالبه تو شب همه چیز دقیقا مثل همون روزه فقط تاریکتر و ترسناک‌تر ",
    " بعضی وقتا فقط دلت می‌خواد یه نفر باشه که واقعاً گوش بده ",
    " هر کی سرش به کار خودشه، ولی انگار همه‌مون یه چیزی کم داریم ",
    " نمی‌دونم داریم به کجا میریم با این همه اتفاق ",
    " بعضی وقتا سکوت بیشتر از حرف زدن آدمو لو میده ",
    " یکی اون پلی‌لیست قدیمی‌ ریمیکس رپی رو بده دوباره، همون که غمگین بود ",
    " همه چی خیلی سریع داره عوض میشه انگار ",
    " این زندگیه یا فقط رد شدن از روزها؟ ",
    "این گیفای باحالو از کجا گیر میارین؟",
    " انگار هیچ جایی دیگه امن نیست ",
    " بعضی شبا فقط باید بذاری موزیک پخش شه و به هیچی فکر نکنی ",
    " امروز از اون روزاست که فقط یه موزیک لایت و یه پتو می‌خواد ",
    " نمی‌دونم چرا ولی حس می‌کنم دیگه مثل قبل نیستیم ",
    " دلم می‌خواد یه بارم همه چی طبق برنامه پیش بره ",
    " حس می‌کنم این چند روز بیشتر از کل ماه گذشته گذشت ",
    " انگار هر چی بیشتر تلاش می‌کنی، فاصله بیشتر میشه ",
    " آدم واقعاً نمی‌دونه باید به چی باور داشته باشه ",
    " بارون داره میاد، یه حس سنگین تو هواست ",
]


async def init_client():
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, 'r') as f:
                session_str = f.read().strip()
            client = TelegramClient(StringSession(session_str), api_id,
                                    api_hash)
            await client.connect()
            print("✅ اتصال با استفاده از session موجود برقرار شد.")
        except Exception as e:
            print(
                f"⚠️ خطا در بارگذاری session: {e} | تلاش برای ایجاد session جدید..."
            )
            client = TelegramClient(StringSession(), api_id, api_hash)
            await client.start(phone_number)
            session_str = client.session.save()
            with open(SESSION_FILE, 'w') as f:
                f.write(session_str)
    else:
        print("📦 فایل session پیدا نشد. در حال ساخت session جدید...")
        client = TelegramClient(StringSession(), api_id, api_hash)
        await client.start(phone_number)
        session_str = client.session.save()
        with open(SESSION_FILE, 'w') as f:
            f.write(session_str)

    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        code = input("📩 لطفاً کد تأیید را وارد کنید: ")
        await client.sign_in(phone_number, code)

    return client

def remove_link_from_file(file_path, target_link):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r') as f:
        lines = f.readlines()
    with open(file_path, 'w') as f:
        for line in lines:
            if line.strip() != target_link.strip():
                f.write(line)

async def join_and_test(client, link):
    attempt = 0  # شمارش تعداد تلاش‌ها

    while attempt < MAX_TRIES:
        attempt += 1
        try:
            print(f"🚪 در حال تلاش برای پیوستن به: {link}")
            if '/+' in link or 'joinchat' in link:
                invite_hash = link.split('/')[-1].replace('+', '')
                try:
                    entity = await client(ImportChatInviteRequest(invite_hash))
                    print("✅ با موفقیت به گروه/کانال با لینک دعوت پیوستیم.")
                except Exception as e:
                    print(f"❌ خطا در جوین شدن با لینک دعوت: {e}")
                    if "has expired" in str(e):
                        remove_link_from_file(LINKS_FILE, link)
                    with open("unable_to_join.txt", 'a') as f:
                        f.write(link + '\n')
                    break
            else:
                username = link.split('/')[-1]
                entity = await client.get_entity(username)
                await client(JoinChannelRequest(entity))
                print("✅ با موفقیت به گروه/کانال عمومی پیوستیم.")

            await asyncio.sleep(2)

            # تلاش برای ارسال پیام تست
            try:
                result = await client.send_message(link, "سلام♥")
                real_msg = None
                if isinstance(result, Updates):
                    for update in result.updates:
                        if isinstance(
                                update,
                            (UpdateNewMessage, UpdateNewChannelMessage)):
                            real_msg = update.message
                            break
                else:
                    real_msg = result

                await asyncio.sleep(10)

                # بررسی وجود پیام
                if real_msg:
                    msg = await client.get_messages(link, ids=real_msg.id)
                    if msg:
                        print("🔍 پیام با موفقیت از سرور بازیابی شد.")
                    else:
                        print("پیام توسط ربات ها پاک شده است")
                        with open("unable_to_join.txt", 'a') as f:
                            f.write(link + '\n')
                else:
                    print("⚠️ پیامی برای بررسی نداشتیم.")
            except Exception as e:
                print(f"❌ خطا: {e}")
                with open("unable_to_join.txt", 'a') as f:
                    f.write(link + '\n')
            break
        except FloodWaitError as e:
            # اگر با ارور FloodWaitError مواجه شدیم، منتظر می‌مانیم و دوباره تلاش می‌کنیم
            print(f"❌ نیاز به صبر {e.seconds} ثانیه است. منتظر می‌مانیم.")
            await asyncio.sleep(e.seconds)

        except Exception as e:
            msg = str(e)
            if "already a participant" in msg:
                print("ℹ️ کاربر قبلاً عضو این گروه بوده.")
                break  # نیازی به تلاش مجدد نیست
            elif "A wait of" in msg and "is required" in msg:
                seconds = int(''.join([c for c in msg if c.isdigit()]))
                print(f"⏳ نیاز به صبر {seconds} ثانیه. صبر می‌کنیم...")
                await asyncio.sleep(seconds)
                continue
            else:
                print(f"❌ خطا در جوین شدن به {link}: {e}")
                with open("unable_to_join.txt", 'a') as f:
                    f.write(link + '\n')

        # اگر تعداد تلاش‌ها کمتر از MAX_TRIES باشد، کمی صبر می‌کنیم
        if attempt < MAX_TRIES - 1:
            print(f"🔄 تلاش مجدد در {WAIT_TIME} ثانیه دیگر...")
            await asyncio.sleep(WAIT_TIME)

async def get_total_dialogs_count(client):
    dialogs = await client.get_dialogs()
    count = sum(1 for dialog in dialogs if getattr(dialog.entity, 'megagroup', False) or getattr(dialog.entity, 'broadcast', False))
    return count

async def get_all_groups(client):
    dialogs = await client.get_dialogs()
    groups = [dialog for dialog in dialogs
              if isinstance(dialog.entity, Channel) and dialog.entity.megagroup]
    return groups

async def send_to_groups(client):
    """ارسال پیام به تمام گروه‌ها"""
    try:
        groups = await get_all_groups(client)
        if not groups:
            print("⚠️ هیچ گروهی یافت نشد!")
            return

        print(f"✅ تعداد گروه‌های یافت شده: {len(groups)}")

        message = random.choice(messages_list)
        print(f"\n📤 ارسال پیام انتخاب‌شده: {message}")

        success_count = 0
        counter = 0
        me = await client.get_me()

        for group in groups:
            counter += 1
            if counter >= 5:
                await asyncio.sleep(3)
                counter = 0

            # بررسی ۵ پیام آخر برای جلوگیری از اسپم
            skip = False
            async for msg in client.iter_messages(group.entity, limit=5):
                if msg.sender_id == me.id:
                    print(f"   ⚠️ پیام اخیر خودمان در {group.title} یافت شد، ارسال نمی‌شود.")
                    skip = True
                    break
            if skip:
                continue

            try:
                await client.send_message(group.entity, message)
                print(f"   ✓ ارسال به {group.title}")
                success_count += 1
            except Exception as e:
                print(f"   ✕ خطا در ارسال به {group.title}: {e}")

        print(f"\n📊 نتیجه: {success_count}/{len(groups)} گروه با موفقیت دریافت کردند")

    except Exception as e:
        print(f"❌ خطای سیستمی: {e}")


async def main():
    client = await init_client()

    with open('links.txt', 'r') as f:
        links = [line.strip() for line in f if line.strip()]

    index = 0
    counter_send = 0
    while index < len(links):
        total = await get_total_dialogs_count(client)
        if total >= 475:
            print(f"🚫 به حداکثر تعداد عضویت (475) رسیدیم. در حالت انتظار قرار می‌گیریم...")
            while total >= 475:
                print("⏳ در حال بررسی هر ۳ دقیقه برای ادامه...")
                await asyncio.sleep(180)  # 3 دقیقه صبر
                total = await get_total_dialogs_count(client)
            print("✅ ظرفیت آزاد شد، ادامه می‌دهیم...")
        success = False
        for attempt in range(3):
            if index >= len(links):
                break
            link = links[index]
            try:
                await join_and_test(client, link)
                success = True
                index += 1  # برو به لینک بعدی و تلاش کن
                await asyncio.sleep(1200)
                counter_send += 1
                if counter_send >= 2:
                    counter_send = 0
                    await send_to_groups(client)
                    
                break  # از حلقه بیرون برو چون موفق شدیم
            except:
                break
        if not success:
            print(
                "⏳ سه تلاش انجام شد ولی هیچ‌کدام موفق نبود. ۲ دقیقه صبر می‌کنیم..."
            )
            await asyncio.sleep(120)

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
