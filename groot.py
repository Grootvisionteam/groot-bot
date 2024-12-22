from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# پیامی که با دستور /start ارسال می‌شود
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # ایجاد دکمه‌های Inline با آیکن‌ها برای نمایش در چت
    keyboard = [
        [InlineKeyboardButton("🚀 شروع", callback_data="start_interaction")],
        [InlineKeyboardButton("ℹ️ راهنما", callback_data="help")],
        [InlineKeyboardButton("📞 تماس با پشتیبانی", callback_data="support")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # ارسال پیام خوشامدگویی با دکمه‌ها
    await update.message.reply_text(
        "سلام! به ربات ما خوش آمدید. لطفاً یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=reply_markup
    )

# هندلر کلیک روی دکمه‌ها
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # پیام‌های مختلف بر اساس گزینه انتخاب شده
    if query.data == "start_interaction":
        await query.message.reply_text("شما در حال شروع تعامل با ربات هستید. انتخاب کنید:")
    elif query.data == "help":
        await query.message.reply_text("در اینجا می‌توانید راهنمایی‌های مختلف دریافت کنید.")
    elif query.data == "support":
        await query.message.reply_text("لطفاً پیام خود را برای پشتیبانی ارسال کنید. ما در سریع‌ترین زمان پاسخ خواهیم داد.")
        # ذخیره وضعیت پشتیبانی برای شناسایی پیام‌های بعدی
        context.user_data['support'] = True

# هندلر برای دریافت پیام‌های پشتیبانی
async def handle_support_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # بررسی اینکه آیا کاربر در حال ارسال پیام پشتیبانی است
    if context.user_data.get('support', False):
        # ارسال پیام پشتیبانی به آیدی تلگرام شما
        your_telegram_id = "https://t.me/grootvision"
        await context.bot.send_message(
            chat_id=your_telegram_id,
            text=f"پشتیبانی جدید از کاربر {update.message.from_user.username}:\n\n{update.message.text}"
        )
        # پاسخ دادن به کاربر
        await update.message.reply_text("پیام شما ارسال شد. به زودی با شما تماس خواهیم گرفت.")
        # غیرفعال کردن حالت پشتیبانی پس از ارسال پیام
        context.user_data['support'] = False

# راه‌اندازی ربات
if __name__ == "__main__":
    TOKEN = "7831530422:AAFJwl8Li5mFxmRMLzvGA98zQYu4LB6kGsY"
    app = ApplicationBuilder().token(TOKEN).build()

    # اضافه کردن هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_support_message))  # دریافت پیام‌ها برای پشتیبانی

    print("ربات شما روشن است!")
    app.run_polling()
