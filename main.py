import logging
import random
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "9255718581:AAGnJw8oIilwjQX4PuRYuF4QxoJhOlaOxrc"
ADMIN_ID = 6109069314
NEW_SFG2_MOD_URL = "https://t.me/SFG2UZBEKCHACHITLAR/64"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

all_users = {}
banned_users = set()
user_quiz_step = {}

# 🔥 Haqiqiy PRO o'yinchilar uchun 10 ta qiyin savol
QUIZ_QUESTIONS = [
    {
        "question": "1️⃣ SFG2 o'yinining dastlabki versiyalarida asosiy menyu fonidagi musiqa yoki tovush qaysi afsonaviy o'yinni eslatardi?",
        "options": ["CS 1.6 / CS:S", "Call of Duty", "PUBG Mobile", "Free Fire"],
        "correct": 0
    },
    {
        "question": "2️⃣ SFG2 da snayper miltig'i bilan o'q uzgandan so'ng ikkinchi marta tez otish uchun pichoqqa o'tib yana qaytish (Fast Switch) qanday bajariladi?",
        "options": ["Tezkor qurol almashtirish tugmasi orqali", "Faqat sakrash bilan", "Faqat o'tirish bilan", "O'qni tashlab yuborish bilan"],
        "correct": 0
    },
    {
        "question": "3️⃣ SFG2 da qaysi xarita (map) eng tor yo'laklarga ega bo'lib, asosan snayperlar jangiga mo'ljallangan?",
        "options": ["Awp_lego", "Dust2_long", "Crossfire", "Bikini"],
        "correct": 0
    },
    {
        "question": "4️⃣ Agar o'yinda o'yinchi dushmanning boshiga (Headshot) pistoletda yaqin masofadan o'q uzsa, qanday zarar berish mexanizmi ishlaydi?",
        "options": ["Maksimal kritikal zarar", "Minimal zarar", "Zarar bermaydi", "Faqat zirhni oladi"],
        "correct": 0
    },
    {
        "question": "5️⃣ SFG2 fizikasida granata devordan urilib qaytganda uning portlash vaqti qanday hisoblanadi?",
        "options": ["Tashlangan vaqtdan boshlab 3 soniya", "Devorga tekkan nanosekunddan", "Portlash masofasiga qarab", "Faqat yerga tushganda"],
        "correct": 0
    },
    {
        "question": "6️⃣ SFG2 da maxsus server ochganda, o'yinchi maksimal nechta botni o'yinga qo'sha oladi (standart cheklov)?",
        "options": ["Karta sig'imiga qarab 8 tadan 16 tagacha", "Cheklanmagan", "Faqat 2 ta", "Faqat 5 ta"],
        "correct": 0
    },
    {
        "question": "7️⃣ SFG2 dagi 'Deagle' pistoletining o'q zaxirasi va bitta magazindagi o'qlar soni qancha?",
        "options": ["Magazinda 7 ta, zaxirada 35 ta", "Magazinda 30 ta, zaxirada 90 ta", "Magazinda 12 ta, zaxirada 24 ta", "Magazinda 20 ta, zaxirada 40 ta"],
        "correct": 0
    },
    {
        "question": "8️⃣ SFG2 da qaysi rejim (mode) o'yinchilarga faqat pichoq bilan jang qilish imkonini beradi?",
        "options": ["Knife Round / Knife Mode", "Deathmatch", "Bomb Mode", "Zombi Mode"],
        "correct": 0
    },
    {
        "question": "9️⃣ SFG2 da zirh (Kevlar + Helmet) sotib olganda u dushmanning qaysi qismidan keladigan zararni kamaytiradi?",
        "options": ["Bosh va tanadan keladigan o'q zararini", "Faqat oyoq zararini", "Faqat pichoq zararini", "Granata portishini yo'q qiladi"],
        "correct": 0
    },
    {
        "question": "🔟 Barcha 10 ta qiyin savolga mukammal javob berib, chinakam SFG2 ustasi ekanligingizni isbotlashga tayyormisiz?",
        "options": ["Ha, albatta! Men pro o'yinchiman 🏆", "Yo'q", "Qiyin ekan", "Taslim bo'laman"],
        "correct": 0
    }
]

def get_kb(uid):
    m = InlineKeyboardMarkup(row_width=1)
    m.add(
        InlineKeyboardButton("🎯 Qiyin Viktorina (10 ta savol)", callback_data="start_quiz"),
        InlineKeyboardButton("🎮 SFG2 Modlarini olish", callback_data="mods"),
        InlineKeyboardButton("🚗 Car Parking Akkaunt (50k)", callback_data="car"),
        InlineKeyboardButton("🌸 Anime videolar (1-5 qism)", callback_data="anime"),
        InlineKeyboardButton("🎁 Kundalik Bonus", callback_data="bonus"),
        InlineKeyboardButton("📢 Rasmiy Kanalimiz", url="https://t.me/Kontr_2_Modlari"),
        InlineKeyboardButton("ℹ️ Bot haqida", callback_data="about")
    )
    if uid == ADMIN_ID:
        m.add(InlineKeyboardButton("👑 Admin Panel", callback_data="panel"))
    return m

@dp.message_handler(commands=["start"])
async def start_cmd(msg: types.Message):
    uid = msg.from_user.id
    if uid in banned_users and uid != ADMIN_ID:
        await msg.reply("🚫 Kechirasiz, siz botdan bloklangansiz.")
        return
    all_users[uid] = msg.from_user.full_name
    
    # Salomlashish stikeri (xavfsiz tarzda)
    try:
        await bot.send_sticker(uid, sticker="CAACAgIAAxkBAAE2g3hnZ5...")
    except:
        pass

    await msg.reply(
        f"Assalomu alaykum, **{msg.from_user.full_name}**! 🔥🎮\n\n"
        "Boshqaruv paneliga xush kelibsiz. AGAR 10 TA QIYIN SAVOLGA TO'G'RI JAVOB BERSANGIZ, MAXSUS SFG2 MOD (64-chi post) BERILADI! 🎁\n\n"
        "Kerakli bo'limni tanlang:",
        reply_markup=get_kb(uid),
        parse_mode="Markdown"
    )

@dp.callback_query_handler(text="back")
async def back_cb(cq: types.CallbackQuery):
    await bot.answer_callback_query(cq.id)
    await cq.message.edit_text(
        "📂 **Asosiy menyu:**\n\nKerakli bo'limni tanlang:",
        reply_markup=get_kb(cq.from_user.id),
        parse_mode="Markdown"
    )

# --- QIYIN VIKTORINA TIZIMI ---
@dp.callback_query_handler(text="start_quiz")
async def start_quiz_cb(cq: types.CallbackQuery):
    uid = cq.from_user.id
    user_quiz_step[uid] = 0
    await bot.answer_callback_query(cq.id, text="Qiyin viktorina boshlandi! Aqlingizni sinang! 🧠")
    await send_quiz_question(cq.message, uid, 0)

async def send_quiz_question(message, uid, q_index):
    if q_index >= len(QUIZ_QUESTIONS):
        try:
            # 10 ta savol tugaganda xursand qiluvchi stiker
            await bot.send_sticker(uid, sticker="CAACAgIAAxkBAAE2g3xnZ5...")
        except:
            pass

        kb = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Asosiy menyu", callback_data="back"))
        prize_text = (
            "🎉 **OYHOO! QOYIL, BOSS! SIZ BARCHA 10 TA QIYIN SAVOLGA TO'G'RI JAVOB BERDINGIZ!** 🏆🔥\n\n"
            f"Va'da qilinganidek, sizga eng yangi va maxsus SFG2 mod havolasi taqdim etiladi:\n\n"
            f"🔗 **{NEW_SFG2_MOD_URL}**\n\n"
            "G'alaba muborak bo'lsin! 🎮✨"
        )
        try:
            await message.edit_text(prize_text, reply_markup=kb, parse_mode="Markdown")
        except:
            await message.answer(prize_text, reply_markup=kb, parse_mode="Markdown")
        return

    q = QUIZ_QUESTIONS[q_index]
    kb = InlineKeyboardMarkup(row_width=1)
    for idx, opt in enumerate(q["options"]):
        kb.add(InlineKeyboardButton(opt, callback_data=f"qans_{q_index}_{idx}"))
    
    # Admin uchun savolni o'tkazib yuborish tugmasi
    if uid == ADMIN_ID:
        kb.add(InlineKeyboardButton("⏭ Savolni o'tkazib yuborish (Admin)", callback_data=f"skip_{q_index}"))
        
    kb.add(InlineKeyboardButton("❌ Viktorinani to'xtatish", callback_data="back"))

    text = f"🎯 **SFG2 PRO Viktorinasi ({q_index + 1}/10):**\n\n{q['question']}"
    try:
        await message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    except:
        await message.answer(text, reply_markup=kb, parse_mode="Markdown")

@dp.callback_query_handler(text_startswith="skip_")
async def skip_question_cb(cq: types.CallbackQuery):
    if cq.from_user.id != ADMIN_ID:
        return
    uid = cq.from_user.id
    q_idx = int(cq.data.split("_")[1])
    next_q = q_idx + 1
    user_quiz_step[uid] = next_q
    await bot.answer_callback_query(cq.id, text="Savol o'tkazib yuborildi! ⏭", show_alert=True)
    await send_quiz_question(cq.message, uid, next_q)

@dp.callback_query_handler(text_startswith="qans_")
async def answer_quiz_cb(cq: types.CallbackQuery):
    uid = cq.from_user.id
    data_parts = cq.data.split("_")
    q_idx = int(data_parts[1])
    chosen_opt = int(data_parts[2])

    correct_opt = QUIZ_QUESTIONS[q_idx]["correct"]

    if chosen_opt == correct_opt:
        await bot.answer_callback_query(cq.id, text="Dahshat! To'g'ri topdingiz! ✅🔥")
        
        try:
            # Har bir to'g'ri javob uchun xursand qiluvchi stiker yuborish
            await bot.send_sticker(uid, sticker="CAACAgIAAxkBAAE2g3hnZ5...")
        except:
            pass

        next_q = q_idx + 1
        user_quiz_step[uid] = next_q
        await send_quiz_question(cq.message, uid, next_q)
    else:
        await bot.answer_callback_query(cq.id, text="Notog'ri javob! Faqat to'g'ri javoblar bilan o'tish mumkin.", show_alert=True)
        kb = InlineKeyboardMarkup().add(
            InlineKeyboardButton("🔄 Qaytadan urinib ko'rish", callback_data="start_quiz"),
            InlineKeyboardButton("🔙 Asosiy menyu", callback_data="back")
        )
        await cq.message.edit_text(
            "❌ **Afsus, noto'g'ri javob berdingiz!**\n\n"
            "Mukofotni qo'lga kiritish uchun 10 ta savolning **barchasiga to'g'ri** javob berishingiz shart. Qaytadan urinib ko'ring:",
            reply_markup=kb,
            parse_mode="Markdown"
        )

# --- ADMIN PANEL ---
@dp.callback_query_handler(text="panel")
async def panel_cb(cq: types.CallbackQuery):
    if cq.from_user.id != ADMIN_ID:
        await bot.answer_callback_query(cq.id, text="Bu bo'lim faqat admin uchun!", show_alert=True)
        return
    await bot.answer_callback_query(cq.id)
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📊 Jonli Statistika", callback_data="stats"),
        InlineKeyboardButton("👥 Foydalanuvchilar & Ban", callback_data="users"),
        InlineKeyboardButton("🔙 Asosiy Menyuga Qaytish", callback_data="back")
    )
    await cq.message.edit_text(
        "👑 **SUPER ADMIN PANELIGA XUSH KELIBSISIZ, BOSS!**\n\nKerakli bo'limni tanlang: 👇",
        reply_markup=kb,
        parse_mode="Markdown"
    )

@dp.callback_query_handler(text="stats")
async def stats_cb(cq: types.CallbackQuery):
    if cq.from_user.id != ADMIN_ID: return
    await bot.answer_callback_query(cq.id)
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Admin Panel", callback_data="panel"))
    t = (
        f"📊 **Botning Jonli Statistikasi:**\n\n"
        f"👥 Jami foydalanuvchilar: **{len(all_users)} ta**\n"
        f"🚫 Bloklanganlar: **{len(banned_users)} ta**\n"
        f"⚡ Bot holati: **Ishlayapti (Online) ✅**"
    )
    await cq.message.edit_text(t, reply_markup=kb, parse_mode="Markdown")

@dp.callback_query_handler(text="users")
async def users_cb(cq: types.CallbackQuery):
    if cq.from_user.id != ADMIN_ID: return
    await bot.answer_callback_query(cq.id)
    kb = InlineKeyboardMarkup(row_width=1)
    for uid, name in list(all_users.items())[:15]:
        st = " [BLOKLANGAN 🚫]" if uid in banned_users else ""
        kb.add(InlineKeyboardButton(f"👤 {name}{st}", callback_data="none"))
        if uid != ADMIN_ID:
            if uid in banned_users:
                kb.add(InlineKeyboardButton(f"✅ Unban ({name})", callback_data=f"unban_{uid}"))
            else:
                kb.add(InlineKeyboardButton(f"🚫 Ban qilish ({name})", callback_data=f"ban_{uid}"))
    kb.add(InlineKeyboardButton("🔙 Admin Panel", callback_data="panel"))
    await cq.message.edit_text(
        "👥 **Bot foydalanuvchilari va boshqaruvi:**",
        reply_markup=kb,
        parse_mode="Markdown"
    )

@dp.callback_query_handler(text_startswith="ban_")
async def ban_cb(cq: types.CallbackQuery):
    if cq.from_user.id != ADMIN_ID: return
    banned_users.add(int(cq.data.split("_")[1]))
    await bot.answer_callback_query(cq.id, text="Foydalanuvchi bloklandi! 🚫", show_alert=True)
    await users_cb(cq)

@dp.callback_query_handler(text_startswith="unban_")
async def unban_cb(cq: types.CallbackQuery):
    if cq.from_user.id != ADMIN_ID: return
    uid = int(cq.data.split("_")[1])
    if uid in banned_users: banned_users.remove(uid)
    await bot.answer_callback_query(cq.id, text="Foydalanuvchi blokdan chiqarildi! ✅", show_alert=True)
    await users_cb(cq)

@dp.callback_query_handler(text="none")
async def none_cb(cq: types.CallbackQuery):
    await bot.answer_callback_query(cq.id)

@dp.callback_query_handler(text="mods")
async def mods_cb(cq: types.CallbackQuery):
    await bot.answer_callback_query(cq.id)
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("📸 Instagram", url="https://www.instagram.com/az1zbek000111?obrf=ZTM0YWt2dTVuMGJn"),
        InlineKeyboardButton("🎬 YouTube", url="https://youtube.com/@uzb_rivals?si=WEN3uxqYUI6ElPAD"),
        InlineKeyboardButton("✅ Obuna bo'ldim", callback_data="check_sub"),
        InlineKeyboardButton("🔙 Orqaga", callback_data="back")
    )
    t = (
        "🎮 **SFG2 modini olish shartlari:**\n\n"
        "1️⃣ Instagram va YouTube'ga obuna bo'ling.\n"
        "2️⃣ 'Obuna bo'ldim' tugmasini bosing!"
    )
    await cq.message.edit_text(t, reply_markup=kb, parse_mode="Markdown")

@dp.callback_query_handler(text="check_sub")
async def process_check_sub(cq: types.CallbackQuery):
    await bot.answer_callback_query(cq.id, text="Mod havolasi yuborilmoqda...")
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Asosiy menyu", callback_data="back"))
    await bot.send_message(
        cq.from_user.id,
        f"Mana yangi SFG2 modining havolasi:\n\n🔗 {NEW_SFG2_MOD_URL}\n\nYoqimli o'yin! 🎮",
        reply_markup=kb
    )

@dp.callback_query_handler(text="car")
async def car_cb(cq: types.CallbackQuery):
    await bot.answer_callback_query(cq.id)
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("📸 Adminga yozish", url="https://www.instagram.com/az1zbek000111?cplk=ZTM0YWt2dTVuMGJn"),
        InlineKeyboardButton("🔙 Asosiy menyu", callback_data="back")
    )
    t = (
        "🔥 **CAR PARKING AKKAUNT SOTILADI!** 🔥\n\n"
        "🏎 Zo'r mashinalar va vinillar bor\n"
        "💰 **Narxi:** 50 000 so'm\n"
        "⏳ **10-noyabrgacha skidka!**\n\n"
        "Sotib olish uchun adminga yozing!"
    )
    await bot.send_message(cq.from_user.id, t, reply_markup=kb, parse_mode="Markdown")

@dp.callback_query_handler(text="bonus")
async def bonus_cb(cq: types.CallbackQuery):
    await bot.answer_callback_query(cq.id)
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🎁 Bonusni olish", callback_data="get_bonus"))
    kb.add(InlineKeyboardButton("🔙 Asosiy menyu", callback_data="back"))
    t = (
        "🎁 **Kundalik Bonus bo'limiga xush kelibsiz!**\n\n"
        "Har kuni omadingizni sinab ko'ring va maxsus sovg'alarga ega bo'ling. "
        "Pastdagi tugmani bosing va bonusni qo'lga kiriting! 👇"
    )
    await cq.message.edit_text(t, reply_markup=kb, parse_mode="Markdown")

@dp.callback_query_handler(text="get_bonus")
async def get_bonus_cb(cq: types.CallbackQuery):
    b = [
        "🎉 Tabriklaymiz! Sizga **10,000 so'm** Car Parking chegirmasi berildi! Adminga yozing.",
        f"🔥 Omad! Sizga maxsus SFG2 mod havolasi nasib qildi: {NEW_SFG2_MOD_URL}",
        "⭐ Mukofot: Siz bugun omadlisiz! Keyingi xaridingizga 20% skidka bor.",
        "🚀 Bonus: Do'stlaringizni kanalga taklif qiling va maxsus status yutib oling!"
    ]
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Asosiy menyu", callback_data="back"))
    await bot.answer_callback_query(cq.id, text="Bonus chiqdi!", show_alert=True)
    await bot.send_message(
        cq.from_user.id,
        f"🎁 **Sizning kundalik bonusingiz:**\n\n{random.choice(b)}\n\nErtaga yana urinib ko'ring! ✨",
        reply_markup=kb,
        parse_mode="Markdown"
    )

@dp.callback_query_handler(text="anime")
async def anime_cb(cq: types.CallbackQuery):
    await bot.answer_callback_query(cq.id)
    kb = InlineKeyboardMarkup(row_width=2)
    for i in range(1, 6):
        kb.insert(InlineKeyboardButton(f"{i}-qism 🎬", callback_data=f"an_{i}"))
    kb.add(InlineKeyboardButton("🔙 Asosiy menyu", callback_data="back"))
    await cq.message.edit_text("🌸 **Anime videolar bo'limi:**\n\nQismni tanlang: 👇", reply_markup=kb, parse_mode="Markdown")

@dp.callback_query_handler(text_startswith="an_")
async def an_vid_cb(cq: types.CallbackQuery):
    await bot.answer_callback_query(cq.id)
    p = cq.data.split("_")[1]
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Anime menyusi", callback_data="anime"))
    url = f"https://t.me/ANIMEAMV1/{p}"
    try:
        await bot.send_video(cq.from_user.id, video=url, caption=f"🌸 Anime - {p}-qism\nYoqimli tomosha! ✨", reply_markup=kb)
    except:
        await bot.send_message(cq.from_user.id, text=f"🌸 **Anime - {p}-qism**\n\nHavola:\n🔗 {url}", reply_markup=kb, parse_mode="Markdown")

@dp.callback_query_handler(text="about")
async def about_cb(cq: types.CallbackQuery):
    await bot.answer_callback_query(cq.id)
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 Asosiy menyu", callback_data="back"))
    await bot.send_message(
        cq.from_user.id,
        "ℹ️ **Bot haqida:** SFG2 modlari, Car Parking akkauntlari, animelar va kundalik bonuslar to'plami! 🚀",
        reply_markup=kb,
        parse_mode="Markdown"
    )

if __name__ == "__main__":
    print("Bot muvaffaqiyatli ishga tushdi!")
    executor.start_polling(dp, skip_updates=True)
