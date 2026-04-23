import sys
import django
import logging
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Road24_Bot.settings')
django.setup()

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from asgiref.sync import sync_to_async
from bot.models import (
    ButtonClick, TelegramUser,
    JarimaClick, SugurtaClick, MashinaClick, SmsClick,
    TonirovkaClick, TexClick, MikroClick, SignalClick,
    OneIdClick, SlowClick, DriweClick
)

logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

LANG_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("🇺🇿 O'zbek tili", callback_data="lang_uz")],
    [InlineKeyboardButton("🇷🇺 Русский язык", callback_data="lang_ru")],
])

MAIN_MENU_UZ = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🚔 Jarima va E jarima Ball", callback_data="menu_jarima"),
        InlineKeyboardButton("💰 Mikroqarz", callback_data="menu_mikro"),

    ],
    [
        InlineKeyboardButton("📲 Ilova ishlashi", callback_data="menu_slow"),
        InlineKeyboardButton("📨 SMS kelmadi (ro'yxatdan o'tishda)", callback_data="menu_sms"),

    ],
    [
        InlineKeyboardButton("🛡 Sug'urta", callback_data="menu_sugurta"),
        InlineKeyboardButton("♻️ ONE ID | (ro'yxatdan o'tish)", callback_data="menu_oneid"),
    ],
    [
        InlineKeyboardButton("🕶 Tonirovka", callback_data="menu_tonirovka"),
        InlineKeyboardButton("🚧 Texnik ko'rik", callback_data="menu_tex"),
    ],
    [
        InlineKeyboardButton("🚗  Mashina qo'shish", callback_data="menu_mashina"),
        InlineKeyboardButton("🚨 AvtoSignal", callback_data="menu_signal"),

    ],
    [
        InlineKeyboardButton("🌐 Tilni o'zgartirish", callback_data="change_lang"),
        InlineKeyboardButton("🚗Urban Drive", callback_data="menu_driwe"),
    ],
[
        InlineKeyboardButton("👨‍💼 Operator", callback_data="open_operator"),
    ],


])
JARIMA_MENU_UZ = InlineKeyboardMarkup([
    [InlineKeyboardButton("Jarima Ko'rinmayapti", callback_data="j1")],
    [InlineKeyboardButton("Jarimaga to'ladim, lekin jarima o'chmadi", callback_data="j2")],
    [InlineKeyboardButton("Jarimani qanday to'lash mumkin", callback_data="j3")],
    [InlineKeyboardButton("Jarimadan etiroz", callback_data="j4")],
    [InlineKeyboardButton("To'lov chekini olish", callback_data="j5")],
    [InlineKeyboardButton("To'langan, MIBda faol", callback_data="j6")],
    [InlineKeyboardButton("Barchasiga bir vaqtda to'lash mumkinmi", callback_data="j7")],
    [InlineKeyboardButton("Jarima 48 soatdan keyin keldi", callback_data="j8")],
    [InlineKeyboardButton("Jarima ilovada yoq, (SMS)da keldi", callback_data="j9")],
    [InlineKeyboardButton("YHXX(GAI) bilan bog'lanish", callback_data="j10")],
    [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main")]
])
SUGURTA_MENU_UZ = InlineKeyboardMarkup([
    [InlineKeyboardButton("1️⃣ Sug'urta sotib olish", callback_data="s1")],
    [InlineKeyboardButton("2️⃣ Sug'urta ilovada ko'rinmayapti", callback_data="s2")],
    [InlineKeyboardButton("3️⃣ Sug'urtani bekor qilish", callback_data="s3")],
    [InlineKeyboardButton("4️⃣ Sug'urta turlari", callback_data="s4")],
    [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main")]
])
TONIROVKA_MENU_UZ = InlineKeyboardMarkup([
    [InlineKeyboardButton("1️⃣ Tonirovka: sotib olish, bekor qilish, korinmayapti", callback_data="t1")],
    [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main")]
])
TEX_MENU_UZ = InlineKeyboardMarkup([
    [InlineKeyboardButton("1️⃣ Texnik ko'rik malumoti ko'rinmayapti yoki notog'ri", callback_data="x1")],
    [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main")]
])
MIKRO_MENU_UZ = InlineKeyboardMarkup([
    [InlineKeyboardButton("1️⃣ Mikroqarz qancha vaqt ichida tasdiqlanadi?", callback_data="q1")],
    [InlineKeyboardButton("2️⃣ Mikrokredit olish uchun qanday hujjatlar kerak?", callback_data="q2")],
    [InlineKeyboardButton("3️⃣ Oylik to'lov, vaqti va foiz stavkasi qanday?", callback_data="q3")],
    [InlineKeyboardButton("4️⃣ Kim mikrokredit olishi mumkin?", callback_data="q4")],
    [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main")]
])
SIGNAL_MENU_UZ = InlineKeyboardMarkup([
    [InlineKeyboardButton("1️⃣ AutoSignal nima va vazifasi?", callback_data="a1")],
    [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main")]
])
ONE_ID_UZ = InlineKeyboardMarkup([
    [InlineKeyboardButton("1️⃣ ONE ID dan ro'yxatdan o'tish", callback_data="o1")],
    [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main")]
])
MENU_DRIWE = InlineKeyboardMarkup([
    [InlineKeyboardButton("1️⃣ Shartnoma qanday imzolanadi?", callback_data="b1")],
    [InlineKeyboardButton("2️⃣ Shartnoma tuzish va onlayn imzolash", callback_data="b2")],
    [InlineKeyboardButton("3️⃣ Qanday to'lov usullari mavjud?", callback_data="b3")],
    [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main")]
])

MASHINA_MENU_UZ = InlineKeyboardMarkup([
    [InlineKeyboardButton("1️⃣ Mashina qo'shish", callback_data="f1")],
    [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main")]
])
SMS_MENU_UZ = InlineKeyboardMarkup([
    [InlineKeyboardButton("1️⃣ Ro'yxatdan o'tishda sms kelmadi", callback_data="g1")],
    [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main")]
])
BACK_UZ = InlineKeyboardMarkup([
    [InlineKeyboardButton("⬅️ Orqaga", callback_data="back_main")]
])

MAIN_MENU_RU = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🚗 Добавить автомобил", callback_data="menu_mashina"),
        InlineKeyboardButton("📨 SMS не пришёл (при регистрации)", callback_data="menu_sms"),
    ],
    [
        InlineKeyboardButton("🚔 Штрафы и E-баллы", callback_data="menu_jarima"),
        InlineKeyboardButton("🛡 Страховка", callback_data="menu_sugurta"),
    ],
    [
        InlineKeyboardButton("♻️ ONE ID | (регистрация)", callback_data="menu_oneid"),
        InlineKeyboardButton("🕶 Тонировка", callback_data="menu_tonirovka"),
    ],
    [
        InlineKeyboardButton("🚧 Техосмотр", callback_data="menu_tex"),
        InlineKeyboardButton("💰 Микрозайм", callback_data="menu_mikro"),
    ],
    [
        InlineKeyboardButton("📲 Работа приложения", callback_data="menu_slow"),
        InlineKeyboardButton("🚨 АвтоСигнал", callback_data="menu_signal"),
    ],
    [
        InlineKeyboardButton("🌐 Сменить язык", callback_data="change_lang"),
        InlineKeyboardButton("Урбан Драйв", callback_data="menu_driwe"),
    ],
[
        InlineKeyboardButton("👨‍💼 Оператор", callback_data="open_operator"),
    ],
])

JARIMA_MENU_RU = InlineKeyboardMarkup([
    [InlineKeyboardButton("Штраф не отображается", callback_data="j1")],
    [InlineKeyboardButton("Оплатил штраф, но он не исчез", callback_data="j2")],
    [InlineKeyboardButton("Как оплатить штраф", callback_data="j3")],
    [InlineKeyboardButton("Обжалование штрафа", callback_data="j4")],
    [InlineKeyboardButton("Получить чек об оплате", callback_data="j5")],
    [InlineKeyboardButton("Оплачен, но активен в МИБ", callback_data="j6")],
    [InlineKeyboardButton("Можно ли оплатить все сразу", callback_data="j7")],
    [InlineKeyboardButton("Штраф пришёл через 48 часов", callback_data="j8")],
    [InlineKeyboardButton("Штрафа нет в приложении, пришёл по SMS", callback_data="j9")],
    [InlineKeyboardButton("Связаться с ГИБДД (YHXX)", callback_data="j10")],
    [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
])

SUGURTA_MENU_RU = InlineKeyboardMarkup([
    [InlineKeyboardButton("1️⃣ Купить страховку", callback_data="s1")],
    [InlineKeyboardButton("2️⃣ Страховка не отображается в приложении", callback_data="s2")],
    [InlineKeyboardButton("3️⃣ Отменить страховку", callback_data="s3")],
    [InlineKeyboardButton("4️⃣ Виды страховок", callback_data="s4")],
    [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
])

TONIROVKA_MENU_RU = InlineKeyboardMarkup([
    [InlineKeyboardButton("1️⃣ Тонировка: купить, отменить, не отображается", callback_data="t1")],
    [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
])

TEX_MENU_RU = InlineKeyboardMarkup([
    [InlineKeyboardButton("1️⃣ Данные техосмотра не отображаются или неверны", callback_data="x1")],
    [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
])

MIKRO_MENU_RU = InlineKeyboardMarkup([
    [InlineKeyboardButton("1️⃣ За сколько времени одобряется микрозайм?", callback_data="q1")],
    [InlineKeyboardButton("2️⃣ Какие документы нужны для микрокредита?", callback_data="q2")],
    [InlineKeyboardButton("3️⃣ Ежемесячный платёж, срок и процентная ставка?", callback_data="q3")],
    [InlineKeyboardButton("4️⃣ Кто может получить микрокредит?", callback_data="q4")],
    [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
])

SIGNAL_MENU_RU = InlineKeyboardMarkup([
    [InlineKeyboardButton("1️⃣ Что такое AutoSignal и его назначение?", callback_data="a1")],
    [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
])

ONE_ID_RU = InlineKeyboardMarkup([
    [InlineKeyboardButton("1️⃣ Регистрация через ONE ID", callback_data="o1")],
    [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
])

MASHINA_MENU_RU = InlineKeyboardMarkup([
    [InlineKeyboardButton("1️⃣ Добавить автомобиль", callback_data="f1")],
    [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
])

SMS_MENU_RU = InlineKeyboardMarkup([
    [InlineKeyboardButton("1️⃣ SMS не пришёл при регистрации", callback_data="g1")],
    [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
])
URBAN_DRIWE_RU = InlineKeyboardMarkup([
    [InlineKeyboardButton("1️⃣ Как подписать договор?", callback_data="b1")],
    [InlineKeyboardButton("2️⃣ Договор и онлайн-подписание", callback_data="b2")],
    [InlineKeyboardButton("3️⃣ Какие способы оплаты доступны?", callback_data="b3")],
    [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
])


BACK_RU = InlineKeyboardMarkup([
    [InlineKeyboardButton("⬅️ Назад", callback_data="back_main")]
])

ANSWERS_UZ = {
    "j1": (
        "🚗 Road24 ilovasi orqali avtomobilingizga rasmiylashtirilgan jarimalarni kuzating, tekshiring va to'lang.\n"
        "Qanday ishlaydi:\n"
        "1️⃣ Avtomobilni ilovaga qo'shing — bir necha daqiqa yetarli, ma'lumotlar avtomatik aniqlanadi.\n"
        "2️⃣ YHXX tasdiqlagan jarimalar avtomatik ko'rinadi.\n"
        "3️⃣ Yangi jarimalar haqida push-xabarnoma keladi.\n"
        "Road24 — jarimalarni nazorat qilish va to'lovlarni qulay amalga oshirish uchun ishonchli yordamchi"
    ),
    "j2": (
        "🚗 Hurmatli foydalanuvchi!\n"
        "Agar siz jarima uchun to'lov amalga oshirgan bo'lsangiz, iltimos jarima sahifasiga kirib \"Yangilash\" tugmasini bosing.\n"
        "Agar shundan keyin ham ma'lumotlar yangilanmasa, iltimos Birozdan so'ng qayta urinib ko'ring.\n"
        "Tushunganingiz uchun rahmat"
    ),
    "j3": (
        "1️⃣ Ilovaga kirib Jarimalar bo'limini oching.\n"
        "2️⃣ To'lamoqchi bo'lgan jarimani tanlang.\n"
        "3️⃣ Pastga tushib Yangilash ni bosing.\n"
        "4️⃣ Ma'lumot yangilangach To'lash ni bosing.\n"
        "5️⃣ Karta qo'shilmagan bo'lsa, kartani kiriting va davom eting.\n"
        "6️⃣ Keyingi oynada summa chiqadi va To'lash ni bosing.\n"
        "7️⃣ SMS kodni kiriting va to'lovni tasdiqlang.\n"
        "✅ Tayyor! Jarima to'landi. Xizmat yoqqan bo'lsa, ilovani baholashni unutmang ⭐"
    ),
    "j4": (
        "🛂 Agar jarima noto'g'ri yuborilgan deb hisoblasangiz:\n\n"
        "1️⃣ Qarorda ko'rsatilgan telefon raqamiga qo'ng'iroq qiling.\n"
        "2️⃣ 1102 qisqa raqamiga murojaat qiling.\n"
        "3️⃣ Agar bog'lana olmasangiz, YHXX (GAI) bo'limiga shaxsan boring.\n"
        "4️⃣ Masala hal bo'lmasa, sud orqali jarimani bekor qildirish huquqiga egasiz.\n\n"
        "📞 Markaziy aloqa: 71-207-14-66\n\n"
        "📍 Hududiy markazlar:\n"
        "Toshkent shahri: 95-954-34-32, 95-954-31-37, 95-954-31-36, 95-954-30-39\n"
        "Toshkent viloyati: 55-902-37-76, 55-902-37-80, 55-902-37-79\n\n"
        "Viloyatlar:\n"
        "• Andijon — 74-224-40-05\n• Buxoro — 55-305-29-26\n• Jizzax — 55-151-69-35\n"
        "• Navoiy — 95-603-71-42\n• Namangan — 69-210-40-48\n• Samarqand — 55-707-81-15\n"
        "• Sirdaryo — 55-651-65-21\n• Surxondaryo — 76-228-55-60\n"
        "• Farg'ona — 73-241-57-15, 73-241-57-16\n• Xorazm — 62-224-56-12\n"
        "• Qashqadaryo — 75-221-23-26\n• Qoraqalpog'iston R. — 61-225-80-11\n\n"
        "🕘 Call-markaz ish vaqti: Dushanbadan shanbagacha — 09:00 dan 18:00 gacha"
    ),
    "j5": (
        "🧾 To'lov cheklari tarixi\n"
        "Road24 orqali qilingan barcha to'lov cheklarining tarixini Bosh (Garaj) menyusining pastidagi #To'lovlar bo'limida ko'rishingiz mumkin."
    ),
    "j6": (
        "📩 Hurmatli foydalanuvchi!\n"
        "Holatni tekshirishimiz uchun aynan shu jarima bo'yicha to'lov cheki va jarima qaror raqamini operatorga yuboring."
    ),
    "j7": (
        "Hurmatli foydalanuvchi,\n"
        "Barcha jarimalarni bir vaqtda to'lashdan oldin, iltimos har bir jarimaga alohida kirib, \"Yangilash\" tugmasini bosib ma'lumotlarni yangilab chiqing.\n"
        "Shundan so'ng to'lovni amalga oshirishingizni tavsiya etamiz."
    ),
    "j8": (
        "https://www.instagram.com/reel/DUfn18LjbIy/?igsh=MXYyaXR0dG1rbzZhOA==\n"
        "Shu vidio orqali savolingizga javob olishingiz mumkin. Bizni instagram sahifamizni kuzatib boring."
    ),
    "j9": (
        "Hurmatli foydalanuvchi,\n"
        "Sizga yuzaga kelgan noqulaylik uchun avvalo uzr so'raymiz.\n\n"
        "📌 Agar jarima avtomobilga emas, balki to'g'ridan-to'g'ri jismoniy shaxsga rasmiylashtirilgan bo'lsa, "
        "ushbu turdagi jarimalar hozirda Road24 ilovasida aks etmaydi.\n\n"
        "👉 Bunday jarimalar odatda SMS, pochta yoki boshqa davlat tizimlari orqali yuboriladi.\n\n"
        "📲 Road24 hozirda asosan avtomobil raqamiga biriktirilgan jarimalarni ko'rsatadi.\n"
        "🙏 Agar yana savollar tug'ilsa — doim yordamingizdamiz."
    ),
    "j10": (
        "📞 Markaziy aloqa: 71-207-14-66\n\n"
        "📍 Hududiy markazlar:\n"
        "Toshkent shahri: 95-954-34-32, 95-954-31-37, 95-954-31-36, 95-954-30-39\n"
        "Toshkent viloyati: 55-902-37-76, 55-902-37-80, 55-902-37-79\n\n"
        "Viloyatlar:\n"
        "• Andijon — 74-224-40-05\n• Buxoro — 55-305-29-26\n• Jizzax — 55-151-69-35\n"
        "• Navoiy — 95-603-71-42\n• Namangan — 69-210-40-48\n• Samarqand — 55-707-81-15\n"
        "• Sirdaryo — 55-651-65-21\n• Surxondaryo — 76-228-55-60\n"
        "• Farg'ona — 73-241-57-15, 73-241-57-16\n• Xorazm — 62-224-56-12\n"
        "• Qashqadaryo — 75-221-23-26\n• Qoraqalpog'iston R. — 61-225-80-11\n\n"
        "🕘 Call-markaz ish vaqti: Dushanbadan shanbagacha — 09:00 dan 18:00 gacha"
    ),
    "s1": (
        "🚗 Road24 ilovasi orqali Sug'urta polisini sotib olishdan oldin:\n\n"
        "1️⃣ Sug'urta turini to'g'ri tanlang.\n"
        "2️⃣ Sug'urta muddati — boshlanish sanasi va amal qilish muddatini belgilang.\n"
        "3️⃣ Cheklangan turdagi sug'urta uchun kamida bitta haydovchi ma'lumotlari kiritilishi shart.\n"
        "4️⃣ Ma'lumotlarning to'g'riligiga ishonch hosil qiling.\n"
        "5️⃣ Sug'urta narxi kiritilgan ma'lumotlarga qarab avtomatik shakllanadi.\n\n"
        "📩 Texnik muammo yuzaga kelsa, Road24 texnik yordami yoki Sug'urta tashkilotiga murojaat qiling."
    ),
    "s2": (
        "Sug'urta menyusiga kirib, \"Yangilash\" tugmasini bosing.\n"
        "Tashqi tizimlar orqali sotib olingan sug'urta odatda 48–72 soat ichida yangilanadi.\n"
        "Agar yangilangan sug'urta polisi ilovada ko'rinmasa, iltimos bizga quyidagilarni yuboring:\n"
        "- Sug'urta polisi hujjati\n"
        "- To'lov cheki"
    ),
    "s3": (
        "🚦 Sug'urtani bekor qilish tartibi\n\n"
        "1️⃣ Sug'urtani bekor qilish Road24 ilovasi orqali amalga oshirilmaydi — bevosita Sug'urta tashkiloti orqali amalga oshiriladi.\n"
        "Buning uchun Sug'urta polisingiz PDF faylida ko'rsatilgan telefon raqamlarga murojaat qiling.\n\n"
        "2️⃣ Sug'urtani bekor qilish, to'lovni qaytarish yoki haydovchi qo'shish bo'yicha Sug'urta tashkiloti vakillari yordam beradi."
    ),
    "s4": (
        "Cheklangan sug'urta — faqat ro'yxatga kiritilgan haydovchilar mashinani boshqarishi mumkin.\n\n"
        "🔹 Ro'yxatda yo'q haydovchi YTX sodir etsa — sug'urta kuchga kirmaydi.\n"
        "📉 Afzalligi: Arzonroq.\n\n"
        "Cheklanmagan sug'urta — avtomobilni istalgan yaqin qarindosh boshqarishi mumkin.\n\n"
        "🔹 Sug'urta avtomobilga beriladi, haydovchiga emas.\n"
        "📈 Afzalligi: Erkinlik — yaqinlaringiz boshqarishi mumkin."
    ),
    "t1": (
        "Hozirda siz so'ragan muammo bo'yicha Ilovamizda #Profilaktika ishlari olib borilmoqda. "
        "Sizda yuzaga kelgan noqulayliklar uchun uzur so'raymiz. Muammoni mutaxassislarimiz tez orada bartaraf etishadi."
    ),
    "x1": (
        "✔️ Agar Texnik ko'rik ma'lumotlari yangilangani akkauntingizda ko'rinmasa, "
        "dastlab Ilovaning oxirgi versiyasi ekanligini tekshirib, \"#Yangilash\" tugmasini bosing.\n\n"
        "⚠️ Ma'lumotlar bazaga yuklanishi uchun 1 soatdan 24 soatgacha vaqt kerak bo'ladi. "
        "Ayrim hollarda bir necha kun talab qilinishi mumkin."
    ),
    "q1": "Ariza 5 daqiqa ichida tasdiqlanadi.",
    "q2": "Faqat pasport yoki shaxsni tasdiqlovchi hujjat ma'lumotlari. Qo'shimcha hujjatlar talab qilinmaydi.",
    "q3": (
        "Mikroqarzlar 3 oy muddatga beriladi.\n"
        "Oylik foiz: 7%\n"
        "To'lov summasi kredit summasi va foizga qarab avtomatik hisoblanadi.\n"
        "Rasmiylashtirish davomida sizga to'lov bo'yicha grafik jadval taqdim etiladi."
    ),
    "q4": (
        "O'zbekiston fuqarosi bo'lish\n"
        "Yaxshi kredit tarixi va qarzdorlik kechikmasligi\n"
        "Qarz yuklamasi me'yorida bo'lishi kerak"
    ),
    "o1": (
        "Hozirda siz so'ragan muammo bo'yicha Ilovamizda #Profilaktika ishlari olib borilmoqda. "
        "Sizda yuzaga kelgan noqulayliklar uchun uzur so'raymiz. Muammoni mutaxassislarimiz tez orada bartaraf etishadi."
    ),
    "g1": (
        "📱 SMS xabarnoma haqida\n\n"
        "Agar sizga SMS xabar kelmagan bo'lsa, iltimos SMS kelmagan telefon raqamingizni "
        "bosh menuга qaytib operatorga yuboring."
    ),
    "f1": (
        "🔍 Birinchi navbatda, mashinaning Davlat raqamini va texpasport seriya, raqamini to'g'ri kiritayotganingizni tekshiring.\n"
        "⏱️ Agar texpasport yangi bo'lsa, bazaga qo'shish uchun 24–48 soat vaqt talab qilinishi mumkin."
    ),
    "a1": (
        "🚗 AutoSignal orqali siz boshqa haydovchiga aloqaga chiqishingiz mumkin!\n\n"
        "🔍 AutoSignal bo'limiga kiring\n"
        "🔢 Xabar yubormoqchi bo'lgan shaxsning mashina davlat raqamini kiriting\n"
        "📲 Hosil bo'lgan oynadan aloqa turini tanlang\n"
        "✅ Xizmatdan foydalaning!\n\n"
        "💰 Xizmat narxi atiga 2 000 UZS xolos!"
    ),
    "menu_slow": (
        "Agar Road24 ilovasiga kirishda qiyinchilikka duch kelgan bo'lsangiz:\n\n"
        "1️⃣ Telefoningizda \"Parvoz rejimi\" ✈️ ni yoqing va bir necha soniyadan so'ng o'chiring.\n"
        "2️⃣ Agar holat o'zgarmasa — ilovani qurilmangizdan o'chirib, qayta yuklab oling.\n"
        "3️⃣ VPN dan foydalanayotgan bo'lsangiz, uni o'chiring.\n"
        "4️⃣ Internet turini (Wi-Fi / mobil internet) o'zgartirib ko'ring.\n\n"
        "📱 Ushbu amallar odatda texnik muammolarni bartaraf etishga yordam beradi."
    ),
"b1": (
    "📝 Shartnoma qanday imzolanadi?\n\n"
    "Avtomobilni tanlab, buyurtma qoldirganingizdan so'ng, buyurtmangiz "
    "\"Profil\" → \"Mening buyurtmalarim\" bo'limiga tushadi.\n"
    "Kerakli buyurtmani tanlab, undagi \"Buyurtmani imzolash\" tugmasini chapdan o'ngga suring.\n"
    "Shundan so'ng yuzni skanerlash oynasi ochiladi. "
    "Jarayon muvaffaqiyatli yakunlangach, buyurtma imzolanadi."
),
"b2": (
    "📄 UrbanDrive'da shartnoma qanday tuziladi va uni onlayn imzolash mumkinmi?\n\n"
    "Ha, UrbanDrive'da shartnoma tuzish va uni onlayn imzolash mumkin.\n"
    "Avtomobil uchun buyurtma yaratilgach, shartnoma avtomatik ravishda shakllantiriladi. "
    "Siz uni \"Mening buyurtmalarim\" bo'limida ko'rishingiz va yuklab olishingiz mumkin.\n"
    "Shuningdek, \"Buyurtmani imzolash\" tugmasi orqali shartnomani elektron tarzda imzolashingiz mumkin."
),
"b3": (
    "💳 UrbanDrive'da qanday to'lov usullari mavjud?\n\n"
    "UrbanDrive'da quyidagi to'lov usullari mavjud:\n"
    "• Naqd pul\n"
    "• Bank kartasi yoki Payme orqali onlayn to'lov\n"
    "• Bo'lib to'lash (muddatli to'lov)\n"
    "• Kredit\n"
    "• Lizing\n\n"
    "Barcha jarayonlar ilova orqali amalga oshiriladi."
),
}

ANSWERS_RU = {
    "j1": (
        "🚗 Через приложение Road24 вы можете отслеживать, проверять и оплачивать штрафы на ваш автомобиль.\n"
        "Как это работает:\n"
        "1️⃣ Добавьте автомобиль в приложение — данные определяются автоматически.\n"
        "2️⃣ Подтверждённые ГИБДД штрафы отображаются автоматически.\n"
        "3️⃣ О новых штрафах приходят push-уведомления.\n"
        "Road24 — надёжный помощник для контроля штрафов и удобной оплаты."
    ),
    "j2": (
        "🚗 Уважаемый пользователь!\n"
        "Если вы оплатили штраф, зайдите на страницу штрафа и нажмите кнопку \"Обновить\".\n"
        "Если данные не обновились — попробуйте позже. Обновление информации может занять некоторое время.\n"
        "Спасибо за понимание."
    ),
    "j3": (
        "1️⃣ Откройте раздел Штрафы в приложении.\n"
        "2️⃣ Выберите нужный штраф.\n"
        "3️⃣ Прокрутите вниз и нажмите \"Обновить\".\n"
        "4️⃣ После обновления нажмите \"Оплатить\".\n"
        "5️⃣ Если карта не добавлена — введите данные карты.\n"
        "6️⃣ Подтвердите сумму и нажмите \"Оплатить\".\n"
        "7️⃣ Введите SMS-код и подтвердите оплату.\n"
        "✅ Готово! Штраф оплачен. Если сервис понравился — не забудьте оценить приложение ⭐"
    ),
    "j4": (
        "🛂 Если вы считаете штраф неправомерным:\n\n"
        "1️⃣ Позвоните по номеру, указанному в постановлении.\n"
        "2️⃣ Обратитесь на короткий номер 1102.\n"
        "3️⃣ Если не удаётся дозвониться — лично посетите отделение ГИБДД.\n"
        "4️⃣ Если вопрос не решён — вы вправе обжаловать штраф через суд.\n\n"
        "📞 Центральный контакт: 71-207-14-66\n\n"
        "📍 Региональные центры:\n"
        "Ташкент (город): 95-954-34-32, 95-954-31-37, 95-954-31-36, 95-954-30-39\n"
        "Ташкентская область: 55-902-37-76, 55-902-37-80, 55-902-37-79\n\n"
        "Регионы:\n"
        "• Андижан — 74-224-40-05\n• Бухара — 55-305-29-26\n• Джизак — 55-151-69-35\n"
        "• Навои — 95-603-71-42\n• Наманган — 69-210-40-48\n• Самарканд — 55-707-81-15\n"
        "• Сырдарья — 55-651-65-21\n• Сурхандарья — 76-228-55-60\n"
        "• Фергана — 73-241-57-15, 73-241-57-16\n• Хорезм — 62-224-56-12\n"
        "• Кашкадарья — 75-221-23-26\n• Каракалпакстан — 61-225-80-11\n\n"
        "🕘 Время работы колл-центра: Пн–Сб — с 09:00 до 18:00"
    ),
    "j5": (
        "🧾 История чеков об оплате\n"
        "Историю всех платежей через Road24 можно найти в разделе #Платежи в нижней части главного меню (Гараж)."
    ),
    "j6": (
        "📩 Уважаемый пользователь!\n"
        "Для проверки ситуации отправьте оператору чек об оплате и номер постановления о штрафе."
    ),
    "j7": (
        "Уважаемый пользователь,\n"
        "Перед оплатой всех штрафов сразу — зайдите в каждый штраф отдельно и нажмите \"Обновить\".\n"
        "После этого рекомендуем произвести оплату."
    ),
    "j8": (
        "https://www.instagram.com/reel/DUfn18LjbIy/?igsh=MXYyaXR0dG1rbzZhOA==\n"
        "Ответ на ваш вопрос можно найти в этом видео. Подписывайтесь на наш Instagram."
    ),
    "j9": (
        "Уважаемый пользователь,\n"
        "Приносим извинения за неудобства.\n\n"
        "📌 Если штраф оформлен не на автомобиль, а на физическое лицо (по паспортным данным) — "
        "такие штрафы пока не отображаются в Road24.\n\n"
        "👉 Подобные штрафы приходят по SMS, письмом или через другие государственные системы.\n\n"
        "📲 Road24 отображает штрафы, привязанные к номеру автомобиля.\n"
        "🙏 Если возникнут вопросы — мы всегда готовы помочь."
    ),
    "j10": (
        "📞 Центральный контакт: 71-207-14-66\n\n"
        "📍 Региональные центры:\n"
        "Ташкент (город): 95-954-34-32, 95-954-31-37, 95-954-31-36, 95-954-30-39\n"
        "Ташкентская область: 55-902-37-76, 55-902-37-80, 55-902-37-79\n\n"
        "Регионы:\n"
        "• Андижан — 74-224-40-05\n• Бухара — 55-305-29-26\n• Джизак — 55-151-69-35\n"
        "• Навои — 95-603-71-42\n• Наманган — 69-210-40-48\n• Самарканд — 55-707-81-15\n"
        "• Сырдарья — 55-651-65-21\n• Сурхандарья — 76-228-55-60\n"
        "• Фергана — 73-241-57-15, 73-241-57-16\n• Хорезм — 62-224-56-12\n"
        "• Кашкадарья — 75-221-23-26\n• Каракалпакстан — 61-225-80-11\n\n"
        "🕘 Время работы: Пн–Сб — с 09:00 до 18:00"
    ),
    "s1": (
        "🚗 Перед покупкой страхового полиса через Road24:\n\n"
        "1️⃣ Правильно выберите тип страховки.\n"
        "2️⃣ Укажите дату начала и срок действия полиса.\n"
        "3️⃣ Для ограниченной страховки необходимо ввести данные минимум одного водителя.\n"
        "4️⃣ Проверьте правильность паспортных данных, водительского удостоверения и данных авто.\n"
        "5️⃣ Стоимость полиса формируется автоматически на основе введённых данных.\n\n"
        "📩 При технических ошибках обратитесь в техподдержку Road24 или страховую организацию."
    ),
    "s2": (
        "Зайдите в меню Страховка и нажмите \"Обновить\".\n"
        "Страховка из сторонних систем обычно обновляется в течение 48–72 часов.\n"
        "Если полис не появился — отправьте нам:\n"
        "- Документ страхового полиса\n"
        "- Чек об оплате"
    ),
    "s3": (
        "🚦 Порядок отмены страховки\n\n"
        "1️⃣ Отмена страховки осуществляется не через Road24, а напрямую через страховую компанию.\n"
        "Обратитесь по номерам телефонов, указанным в PDF-файле вашего полиса.\n\n"
        "2️⃣ Представители страховой компании проконсультируют вас по вопросам отмены, возврата средств или добавления водителей."
    ),
    "s4": (
        "Ограниченная страховка — управлять автомобилем могут только указанные водители.\n\n"
        "🔹 Если за рулём окажется человек не из списка при ДТП — страховка не действует.\n"
        "📉 Преимущество: Дешевле.\n\n"
        "Неограниченная страховка — автомобилем может управлять любой человек из списка родственников.\n\n"
        "🔹 Страховка оформляется на автомобиль, а не на водителя.\n"
        "📈 Преимущество: Свобода — авто могут использовать близкие."
    ),
    "t1": (
        "В настоящее время по вашему запросу в приложении проводятся профилактические работы. "
        "Приносим извинения за неудобства. Наши специалисты устранят проблему в ближайшее время."
    ),
    "x1": (
        "✔️ Если данные техосмотра не обновились в вашем аккаунте — сначала проверьте, "
        "установлена ли последняя версия приложения, затем нажмите \"#Обновить\".\n\n"
        "⚠️ Загрузка данных в базу может занять от 1 часа до 24 часов. "
        "В некоторых случаях — несколько дней."
    ),
    "q1": "Заявка одобряется в течение 5 минут.",
    "q2": "Необходим только паспорт или документ, удостоверяющий личность. Дополнительные документы не требуются.",
    "q3": (
        "Микрозайм выдаётся на срок 3 месяца.\n"
        "Ежемесячная ставка: 7%\n"
        "Сумма платежа рассчитывается автоматически.\n"
        "При оформлении предоставляется график платежей."
    ),
    "q4": (
        "Гражданство Узбекистана.\n"
        "Хорошая кредитная история, отсутствие просрочек.\n"
        "Долговая нагрузка в пределах нормы."
    ),
    "o1": (
        "В настоящее время в приложении проводятся профилактические работы. "
        "Приносим извинения за неудобства. Наши специалисты устранят проблему в ближайшее время."
    ),
    "g1": (
        "📱 Об SMS-уведомлениях\n\n"
        "Если SMS-сообщение не пришло — вернитесь в главное меню и отправьте оператору "
        "номер телефона, на который не поступило сообщение."
    ),
    "f1": (
        "🔍 Прежде всего проверьте правильность введённого госномера и серии/номера техпаспорта.\n"
        "⏱️ Если техпаспорт новый — добавление в базу данных может занять от 24 до 48 часов."
    ),
    "a1": (
        "🚗 Через AutoSignal вы можете связаться с другим водителем!\n\n"
        "🔍 Войдите в раздел AutoSignal\n"
        "🔢 Введите госномер нужного автомобиля\n"
        "📲 Выберите способ связи в появившемся окне\n"
        "✅ Пользуйтесь сервисом!\n\n"
        "💰 Стоимость услуги — всего 2 000 UZS!"
    ),
    "menu_slow": (
        "Если возникли проблемы при входе в приложение Road24:\n\n"
        "1️⃣ Включите режим полёта ✈️ на телефоне и через несколько секунд выключите.\n"
        "2️⃣ Если не помогло — удалите приложение и установите заново.\n"
        "3️⃣ Если используете VPN — отключите его.\n"
        "4️⃣ Смените тип интернета (Wi-Fi / мобильный интернет) и повторите попытку.\n\n"
        "📱 Эти действия, как правило, устраняют технические проблемы с входом в приложение."
    ),
"b1": (
    "📝 Как подписать договор?\n\n"
    "После того как вы выбрали автомобиль и оформили заказ, он появится в разделе "
    "\"Профиль\" → \"Мои заказы\".\n"
    "Выберите нужный заказ и проведите пальцем по кнопке \"Подписать заказ\" слева направо.\n"
    "После этого откроется окно сканирования лица. "
    "После успешного завершения процесса заказ будет подписан."
),
"b2": (
    "📄 Как заключить договор в UrbanDrive и можно ли подписать его онлайн?\n\n"
    "Да, в UrbanDrive можно заключить договор и подписать его онлайн.\n"
    "После создания заказа на автомобиль договор формируется автоматически. "
    "Вы можете просмотреть и скачать его в разделе \"Мои заказы\".\n"
    "Также вы можете подписать договор электронно через кнопку \"Подписать заказ\"."
),
"b3": (
    "💳 Какие способы оплаты доступны в UrbanDrive?\n\n"
    "В UrbanDrive доступны следующие способы оплаты:\n"
    "• Наличные\n"
    "• Онлайн-оплата картой или через Payme\n"
    "• Рассрочка\n"
    "• Кредит\n"
    "• Лизинг\n\n"
    "Все процессы выполняются через приложение."
),
}

@sync_to_async
def get_lang_async(user_id):
    try:
        user = TelegramUser.objects.filter(user_id=user_id).first()
        return user.lang if (user and user.lang) else None
    except Exception:
        return None


@sync_to_async
def set_user_lang(user_id, lang, first_name="", last_name="", username=""):
    user, created = TelegramUser.objects.get_or_create(
        user_id=user_id,
        defaults={
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "lang": lang,
        }
    )
    if not created:
        user.lang = lang
        user.first_name = first_name or user.first_name
        user.last_name = last_name or user.last_name
        user.username = username or user.username
        user.save()


@sync_to_async
def save_button_click(user_id, button_key, button_name):
    try:
        user = TelegramUser.objects.filter(user_id=user_id).first()
        ButtonClick.objects.create(button_key=button_key, button_name=button_name, user=user)
    except Exception as e:
        print("SAVE ERROR:", e)


MENU_MODEL_MAP = {
    "menu_jarima": JarimaClick, "menu_sugurta": SugurtaClick,
    "menu_mashina": MashinaClick, "menu_sms": SmsClick,
    "menu_tonirovka": TonirovkaClick, "menu_tex": TexClick,
    "menu_mikro": MikroClick, "menu_signal": SignalClick,
    "menu_oneid": OneIdClick, "menu_slow": SlowClick,
    "menu_driwe": DriweClick,
}

BUTTON_NAMES = {
    "menu_jarima": "Jarima", "menu_sugurta": "Sug'urta",
    "menu_mashina": "Mashina qo'shish", "menu_sms": "SMS muammo",
    "menu_tonirovka": "Tonirovka", "menu_tex": "Texnik ko'rik",
    "menu_mikro": "Mikroqarz", "menu_signal": "AutoSignal",
    "menu_oneid": "ONE ID", "menu_slow": "Ilova ishlashi",
    "menu_driwe": "Urban Driwe",
}


@sync_to_async
def save_menu_click(user_id, button_key, button_name):
    try:
        model = MENU_MODEL_MAP.get(button_key)
        if model:
            user = TelegramUser.objects.filter(user_id=user_id).first()
            model.objects.create(user=user, button_key=button_key, button_name=button_name)
    except Exception as e:
        print("SAVE MENU ERROR:", e)

@sync_to_async
def save_operator_click(user_id):
    try:
        from bot.models import OperatorClick
        user = TelegramUser.objects.filter(user_id=user_id).first()
        if user:
            OperatorClick.objects.create(
                user=user,
                button_key="operator",
                button_name="👨‍💼 Operator"
            )
    except Exception as e:
        logging.error(f"OPERATOR SAVE ERROR: {e}")


def get_main_menu_by_lang(lang):
    return MAIN_MENU_RU if lang == "ru" else MAIN_MENU_UZ

def get_back_by_lang(lang):
    return BACK_RU if lang == "ru" else BACK_UZ

def get_answers_by_lang(lang):
    return ANSWERS_RU if lang == "ru" else ANSWERS_UZ

def get_menu_by_lang(lang, menu_uz, menu_ru):
    return menu_ru if lang == "ru" else menu_uz

def get_text_by_lang(lang, uz_text, ru_text):
    return ru_text if lang == "ru" else uz_text

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 Tilni tanlang / Выберите язык:",
        reply_markup=LANG_MENU
    )

async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    d = q.data
    user_id = q.from_user.id
    tg_user = q.from_user

    try:
        await q.answer()
    except Exception:
        pass

    try:

        if d == "lang_uz":
            await set_user_lang(user_id, "uz",
                                first_name=tg_user.first_name or "",
                                last_name=tg_user.last_name or "",
                                username=tg_user.username or "")
            await q.edit_message_text(
                "✅ O'zbek tili tanlandi!\n\nKerakli bo'limni tanlang 👇",
                reply_markup=MAIN_MENU_UZ)
            return

        if d == "lang_ru":
            await set_user_lang(user_id, "ru",
                                first_name=tg_user.first_name or "",
                                last_name=tg_user.last_name or "",
                                username=tg_user.username or "")
            await q.edit_message_text(
                "✅ Выбран русский язык!\n\nВыберите нужный раздел 👇",
                reply_markup=MAIN_MENU_RU)
            return

        if d == "change_lang":
            await q.edit_message_text(
                "🌐 Tilni tanlang / Выберите язык:",
                reply_markup=LANG_MENU)
            return


        lang = await get_lang_async(user_id)
        if lang is None:
            await q.edit_message_text(
                "🌐 Tilni tanlang / Выберите язык:",
                reply_markup=LANG_MENU)
            return


        answers = get_answers_by_lang(lang)
        back = get_back_by_lang(lang)
        main_menu = get_main_menu_by_lang(lang)

        if d == "open_operator":
            await save_operator_click(user_id)

            op_text = get_text_by_lang(lang,
                                       "👨‍💼 Operator bilan bog'lanish uchun quyidagi linkka bosing:",
                                       "👨‍💼 Для связи с оператором нажмите на ссылку ниже:")

            op_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    get_text_by_lang(lang, "👨‍💼 Operatorga o'tish", "👨‍💼 Перейти к оператору"),
                    url="https://t.me/Road24assist"
                )],
                [InlineKeyboardButton(
                    get_text_by_lang(lang, "⬅️ Menyuga qaytish", "⬅️ Вернуться в меню"),
                    callback_data="back_main"
                )],
            ])

            await q.edit_message_text(op_text, reply_markup=op_keyboard)
            return

        if d == "back_main":
            await q.edit_message_text(
                get_text_by_lang(lang, "Kerakli bo'limni tanlang 👇", "Выберите нужный раздел 👇"),
                reply_markup=main_menu)
            return

        if d in BUTTON_NAMES:
            await save_button_click(user_id, d, BUTTON_NAMES[d])
            await save_menu_click(user_id, d, BUTTON_NAMES[d])

        if d == "menu_jarima":
            await q.edit_message_text(
                get_text_by_lang(lang, "🚔 Jarima bo'limi:", "🚔 Раздел штрафов:"),
                reply_markup=get_menu_by_lang(lang, JARIMA_MENU_UZ, JARIMA_MENU_RU))

        elif d == "menu_sugurta":
            await q.edit_message_text(
                get_text_by_lang(lang, "🛡 Sug'urta bo'limi:", "🛡 Раздел страховки:"),
                reply_markup=get_menu_by_lang(lang, SUGURTA_MENU_UZ, SUGURTA_MENU_RU))

        elif d == "menu_mashina":
            await q.edit_message_text(
                get_text_by_lang(lang, "🚔 Mashina qo'shish:", "🚔 Добавить автомобиль:"),
                reply_markup=get_menu_by_lang(lang, MASHINA_MENU_UZ, MASHINA_MENU_RU))

        elif d == "menu_sms":
            await q.edit_message_text(
                get_text_by_lang(lang, "📱 SMS bo'limi:", "📱 Раздел SMS:"),
                reply_markup=get_menu_by_lang(lang, SMS_MENU_UZ, SMS_MENU_RU))

        elif d == "menu_tonirovka":
            await q.edit_message_text(
                get_text_by_lang(lang, "🎨 Tonirovka bo'limi:", "🎨 Раздел тонировки:"),
                reply_markup=get_menu_by_lang(lang, TONIROVKA_MENU_UZ, TONIROVKA_MENU_RU))
        elif d == "menu_driwe":
            await q.edit_message_text(
                get_text_by_lang(lang, "UrbanDriwe:", "Использование UrbanDrive:"),
                reply_markup=get_menu_by_lang(lang, MENU_DRIWE, URBAN_DRIWE_RU))

        elif d == "menu_tex":
            await q.edit_message_text(
                get_text_by_lang(lang, "🧰 Texnik ko'rik:", "🧰 Технический осмотр:"),
                reply_markup=get_menu_by_lang(lang, TEX_MENU_UZ, TEX_MENU_RU))

        elif d == "menu_mikro":
            await q.edit_message_text(
                get_text_by_lang(lang, "💰 Mikroqarz:", "💰 Микрозайм:"),
                reply_markup=get_menu_by_lang(lang, MIKRO_MENU_UZ, MIKRO_MENU_RU))

        elif d == "menu_signal":
            await q.edit_message_text(
                get_text_by_lang(lang, "📡 AutoSignal bo'limi:", "📡 Раздел AutoSignal:"),
                reply_markup=get_menu_by_lang(lang, SIGNAL_MENU_UZ, SIGNAL_MENU_RU))

        elif d == "menu_oneid":
            await q.edit_message_text(
                get_text_by_lang(lang, "🛡 ONE ID bo'limi:", "🛡 Раздел ONE ID:"),
                reply_markup=get_menu_by_lang(lang, ONE_ID_UZ, ONE_ID_RU))

        elif d == "menu_slow":
            await q.edit_message_text(answers["menu_slow"], reply_markup=back)

        elif d == "j6":

            j6_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    get_text_by_lang(lang, "👨‍💼 Operator bilan bog'lanish", "👨‍💼 Связаться с оператором"),
                    url="https://t.me/Road24assist")],
                [InlineKeyboardButton(
                    get_text_by_lang(lang, "⬅️ Orqaga", "⬅️ Назад"),
                    callback_data="menu_jarima")]
            ])
            await q.edit_message_text(answers["j6"], reply_markup=j6_keyboard)


        elif d in answers:
            await save_button_click(user_id, d, d)
            await q.edit_message_text(answers[d], reply_markup=back)

    except Exception as e:
        logging.error(f"CALLBACK XATOSI: {e}")



async def business_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.business_message
    if not msg:
        return
    try:
        conn = await context.bot.get_business_connection(msg.business_connection_id)
        logging.info(f"is_enabled: {conn.is_enabled}")
    except Exception as e:
        logging.error(f"CONNECTION XATOSI: {e}")

    IGNORED_IDS = [6694766222]
    if msg.from_user and msg.from_user.id in IGNORED_IDS:
        return

    user_id = msg.from_user.id
    text = msg.text.lower() if msg.text else ""
    business_connection_id = msg.business_connection_id
    user = msg.from_user

    @sync_to_async
    def save_user():
        tg_user, created = TelegramUser.objects.get_or_create(
            user_id=user.id,
            defaults={
                "first_name": user.first_name or "",
                "last_name": user.last_name or "",
                "username": user.username or "",
            }
        )
        tg_user.first_name = user.first_name or ""
        tg_user.last_name = user.last_name or ""
        tg_user.username = user.username or ""
        tg_user.message_count += 1
        tg_user.save()

    await save_user()

    async def send(message_text, markup=None):
        try:
            await context.bot.send_message(
                chat_id=msg.chat.id,
                text=message_text,
                reply_markup=markup,
                business_connection_id=business_connection_id
            )
        except Exception as e:
            logging.warning(f"Xabar yuborib bo'lmadi: {e}")

    lang = await get_lang_async(user_id)
    if lang is None:
        await send("🌐 Tilni tanlang / Выберите язык:", LANG_MENU)
        return

    select_text = get_text_by_lang(lang, "Quyidagi bo'limlardan birini tanlang:", "Выберите один из разделов ниже:")

    if any(w in text for w in ["jarima", "штраф", "to'lash", "tolash", "штрафы"]):
        await send(select_text, get_menu_by_lang(lang, JARIMA_MENU_UZ, JARIMA_MENU_RU))
    elif any(w in text for w in ["sug'urta", "sugurta", "insurance", "страховка", "страховк"]):
        await send(select_text, get_menu_by_lang(lang, SUGURTA_MENU_UZ, SUGURTA_MENU_RU))
    elif any(w in text for w in ["tonirovka", "тонировка", "tinting", "тонир"]):
        await send(select_text, get_menu_by_lang(lang, TONIROVKA_MENU_UZ, TONIROVKA_MENU_RU))
    elif any(w in text for w in ["texnik", "tex ko'rik", "texkorik", "texasmotr", "ko'rik", "техосмотр", "техник"]):
        await send(select_text, get_menu_by_lang(lang, TEX_MENU_UZ, TEX_MENU_RU))
    elif any(w in text for w in ["mikroqarz", "karz", "mikrokredit", "qarz", "kredit", "микрозайм", "микрокредит"]):
        await send(select_text, get_menu_by_lang(lang, MIKRO_MENU_UZ, MIKRO_MENU_RU))
    elif any(w in text for w in ["autosignal", "signal", "haydovchi", "автосигнал"]):
        await send(select_text, get_menu_by_lang(lang, SIGNAL_MENU_UZ, SIGNAL_MENU_RU))
    elif any(w in text for w in ["one id", "oneid", "ro'yxat", "royxat", "регистрация", "one_id"]):
        await send(select_text, get_menu_by_lang(lang, ONE_ID_UZ, ONE_ID_RU))
    else:
        await send(
            get_text_by_lang(lang, "Kerakli bo'limni tanlang 👇", "Выберите нужный раздел 👇"),
            get_main_menu_by_lang(lang)
        )

from pyngrok import ngrok
def main():
    ngrok.set_auth_token("3B76mknjhh1mOYkUdHRy0Ldiewh_iD24zPR6T4HfuvpGhDBU")
    tunnel = ngrok.connect(8443)
    webhook_url = tunnel.public_url
    print(f"🚀 BOT ISHLADI | Webhook: {webhook_url}")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callbacks))
    app.add_handler(MessageHandler(filters.UpdateType.BUSINESS_MESSAGE, business_message))

    app.run_webhook(
        listen="0.0.0.0",
        port=8443,
        webhook_url=webhook_url,
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates = True,
    )

if __name__ == "__main__":
    main()