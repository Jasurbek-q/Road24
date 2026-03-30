from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from django.conf import settings
from asgiref.sync import sync_to_async
from .models import JarimaClick, TonirovkaClick, SugurtaClick, TexClick, TelegramUser

# Foydalanuvchilarni saqlash uchun
kantaktni_saqlash = []

# =========================
# --- Kontakt so'rash tugmasi ---
contact_button = ReplyKeyboardMarkup([
    [KeyboardButton("📱 Kontaktni yuborish", request_contact=True)]
], resize_keyboard=True, one_time_keyboard=True)

# =========================
# --- Asosiy menyu tugmalari ---
main_menu_buttons = [
    ["Jarima", "Sug'urta"],
    ["Tonirovka", "Texnik ko'rik"],
    ["Ilova ishlashi sekin", "Ballik sistema"]
]
main_menu = ReplyKeyboardMarkup(main_menu_buttons, resize_keyboard=True)


# =========================
# --- Foydalanuvchi bazada bormi tekshirish ---
def user_exists(user_id):
    """Foydalanuvchi bazada mavjudligini tekshirish"""
    return any(user['user_id'] == user_id for user in kantaktni_saqlash)


# =========================
# --- Kontaktni bazaga saqlash ---
def save_contact(user_id, phone_number, first_name, last_name=None, username=None):
    """Foydalanuvchi kontaktini bazaga saqlash"""
    user_data = {
        'user_id': user_id,
        'phone_number': phone_number,
        'first_name': first_name,
        'last_name': last_name,
        'username': username
    }
    kantaktni_saqlash.append(user_data)

    # TODO: Django modeliga saqlash uchun
    # from your_app.models import TelegramUser
    # TelegramUser.objects.create(
    #     user_id=user_id,
    #     phone_number=phone_number,
    #     first_name=first_name,
    #     last_name=last_name,
    #     username=username
    # )

    return user_data


# =========================
# --- /start komandasi ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Agar foydalanuvchi bazada bo'lsa, to'g'ridan menyu ko'rsatamiz
    if user_exists(user_id):
        await update.message.reply_text(
            "Xush kelibsiz! 👋\nKerakli bo'limni tanlang 👇",
            reply_markup=main_menu
        )
    else:
        # Yangi foydalanuvchi uchun kontakt so'raymiz
        await update.message.reply_text(
            "Road24 yordamchi botiga xush kelibsiz! 👋\n\n"
            "Davom etish uchun telefon raqamingizni tasdiqlang 📱",
            reply_markup=contact_button
        )


# =========================
# --- Kontakt qabul qilish ---
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    user_id = update.effective_user.id

    # Faqat o'z kontaktini yuborgan bo'lsa qabul qilamiz
    if contact.user_id == user_id:
        # Kontaktni bazaga saqlaymiz
        save_contact(
            user_id=user_id,
            phone_number=contact.phone_number,
            first_name=contact.first_name,
            last_name=contact.last_name,
            username=update.effective_user.username
        )

        # Muvaffaqiyatli xabar va asosiy menyu
        await update.message.reply_text(
            "✅ Kontaktingiz muvaffaqiyatli saqlandi!\n\n"
            "Endi botdan to'liq foydalanishingiz mumkin 👇",
            reply_markup=main_menu
        )
    else:
        # Boshqa birovning kontaktini yuborgan bo'lsa
        await update.message.reply_text(
            "❌ Iltimos, o'zingizning telefon raqamingizni yuboring!",
            reply_markup=contact_button
        )


# =========================
# --- Mijoz matn yuborganda ---
from asgiref.sync import sync_to_async
from .models import (
    JarimaClick, TonirovkaClick, SugurtaClick, TexClick,
    MashinaClick, SmsClick, MikroClick, SignalClick, OneIdClick, SlowClick,
    TelegramUser
)


# ===================== YORDAMCHI FUNKSIYA =====================
async def save_click(model, user_id, button_key, button_name):
    try:
        user = await sync_to_async(TelegramUser.objects.get)(user_id=user_id)
        await sync_to_async(model.objects.create)(
            user=user,
            button_key=button_key,
            button_name=button_name
        )
    except Exception:
        pass


# ===================== MESSAGE HANDLER =====================
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Foydalanuvchi ro'yxatdan o'tmaganmi tekshirish
    if not user_exists(user_id):
        await update.message.reply_text(
            "Avval ro'yxatdan o'tishingiz kerak 📱\n"
            "/start buyrug'ini bosing",
            reply_markup=contact_button
        )
        return

    text = update.message.text

    # --- Ilova ishlashi sekin javobi ---
    if text == "Ilova ishlashi sekin":
        javob = (
            "Agar Road24 ilovasiga kirishda yoki undan foydalanishda qiyinchilikka duch kelgan bo'lsangiz, "
            "quyidagi harakatlarni bajaring:\n\n"
            "1️⃣ Telefoningizda Parvoz rejimi✈️ (Aviarejim) ni yoqing va bir necha soniyadan song ochiring.\n"
            "2️⃣ Agar holat o'zgarmasa — ilovani qurilmangizdan o'chirib, qayta yuklab oling.\n"
            "3️⃣ Agarda siz VPN dan foydalanayotgan bo'lsangiz, bu ilovaga kirish bilan bog'liq muammolarni keltirib chiqarishi mumkin.\n"
            "4️⃣ Bular ham yordam bermasa internet turini (Wi-Fi / mobil internet) o'zgartirib, ilovaga kirishni qayta urinib ko'ring.\n\n"
            "📱 Ushbu amallar odatda ilovaga kirishdagi texnik muammolarni bartaraf etishga yordam beradi."
        )
        return await update.message.reply_text(javob, reply_markup=main_menu)

    # --- Ballik sistema javobi ---
    if text == "Ballik sistema":
        javob = (
            "Ballik sistema orqali siz xaridlar va xizmatlar uchun ball to'plashingiz mumkin. "
            "Har bir xizmat uchun qancha ball berilishi va ularni qanday ishlatish mumkinligi ilova ichida ko'rsatiladi."
        )
        return await update.message.reply_text(javob, reply_markup=main_menu)

    # --- Orqaga qaytish ---
    if text == "⬅️ Orqaga":
        return await update.message.reply_text("Asosiy menyu 👇", reply_markup=main_menu)

    # =========================
    # --- Jarima menyusi ---
    if text == "Jarima":
        await save_click(JarimaClick, user_id, 'menu_jarima', 'Jarima')
        menu = ReplyKeyboardMarkup([
            ["To'lov qildim, jarima hali ham yopilmadi"],
            ["Jarima uchun to'lov qilish imkonsiz"],
            ["Jarima bekor qilingan lekin ilovada yopilmagan"],
            ["Jarimani bekor qilish uchun shikoyat qilish"],
            ["⬅️ Orqaga"]
        ], resize_keyboard=True)
        return await update.message.reply_text(
            "Iltimos sizda bo'layotgan xatolikni tanlang 👇",
            reply_markup=menu
        )

    # =========================
    # --- Tonirovka menyusi ---
    if text == "Tonirovka":
        await save_click(TonirovkaClick, user_id, 'menu_tonirovka', 'Tonirovka')
        menu = ReplyKeyboardMarkup([
            ["Tonirovka sotib ololmayapman"],
            ["Tonirovka sotib oldim bekor qilmoqchiman"],
            ["Road24 ilovasida tonirovka arizasi shakllandi — bekor qilish kerak"],
            ["⬅️ Orqaga"]
        ], resize_keyboard=True)
        return await update.message.reply_text(
            "Sizda qanday savol bor? 👇",
            reply_markup=menu
        )

    # =========================
    # --- Sug'urta menyusi ---
    if text == "Sug'urta":
        await save_click(SugurtaClick, user_id, 'menu_sugurta', "Sug'urta")
        menu = ReplyKeyboardMarkup([
            ["Sug'urta sotib olmoqchiman"],
            ["Sug'urta sotib oldim bekor qilmoqchiman"],
            ["Cheklangan va cheklanmagan sug'urtalar narxi va farqi"],
            ["⬅️ Orqaga"]
        ], resize_keyboard=True)
        return await update.message.reply_text(
            "Sizda qanday savol bor? 👇",
            reply_markup=menu
        )

    # =========================
    # --- Texnik ko'rik menyusi ---
    if text == "Texnik ko'rik":
        await save_click(TexClick, user_id, 'menu_tex', "Texnik ko'rik")
        menu = ReplyKeyboardMarkup([
            ["Texnik ko'rikdan o'tganman lekin ilovada ko'rinmayapti"],
            ["⬅️ Orqaga"]
        ], resize_keyboard=True)
        return await update.message.reply_text(
            "Texnik ko'rik bo'yicha muammoingizni tanlang 👇",
            reply_markup=menu
        )

# =========================
# --- BOTNI ISHGA TUSHIRISH ---
def start_bot():
    application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    # Handlerlarni qo'shamiz
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    return application