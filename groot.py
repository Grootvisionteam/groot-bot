from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# پیام خوشامدگویی با دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("سلام", callback_data="greet")],
        [InlineKeyboardButton("حجم", callback_data="check_volume")],
        [InlineKeyboardButton("تمدید", callback_data="renew")],
        [InlineKeyboardButton("خرید اکانت", callback_data="buy_account")],
        [InlineKeyboardButton("پشتیبانی", callback_data="support")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "سلام! من ربات گروت ویژن هستم. لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=reply_markup
    )

# هندلر کلیک روی دکمه‌ها
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    # پیام‌های مختلف بر اساس گزینه انتخاب شده
    if query.data == "greet":
        await query.message.reply_text("سلام من گروت ویژن هستم، چه کمکی از دستم برمیاد براتون؟")
    elif query.data == "check_volume":
        await query.message.reply_text("حجم وی‌پی‌ان شما در حال بررسی است، در سریع‌ترین زمان ممکن براتون ارسال میشه.")
    elif query.data == "renew":
        await query.message.reply_text("برای تمدید وی‌پی‌ان‌تون کافیه که اسکرین‌شات واریزی‌تون رو ارسال کنید.")
    elif query.data == "buy_account":
        # نمایش دکمه‌های جدید برای مدت زمان
        durations = [
            [InlineKeyboardButton("1 ماهه", callback_data="1_month")],
            [InlineKeyboardButton("3 ماهه", callback_data="3_months")],
            [InlineKeyboardButton("6 ماهه", callback_data="6_months")],
            [InlineKeyboardButton("1 ساله", callback_data="1_year")]
        ]
        reply_markup = InlineKeyboardMarkup(durations)
        await query.message.reply_text("لطفاً مدت زمان مورد نیاز رو انتخاب کنید:", reply_markup=reply_markup)
    elif query.data == "support":
        await query.message.reply_text("در صورت سوال، ابهام یا چالش با نصب و خدمات وی‌پی‌ان برامون پیام بزارید. در سریع‌ترین زمان پاسخ میدیم.")

    # هندلر انتخاب مدت زمان اکانت
    if query.data in ["1_month", "3_months", "6_months", "1_year"]:
        # دکمه‌های میزان حجم
        volumes = [
            [InlineKeyboardButton("50 گیگ", callback_data="50GB")],
            [InlineKeyboardButton("100 گیگ", callback_data="100GB")],
            [InlineKeyboardButton("200 گیگ", callback_data="200GB")],
        ]
        reply_markup = InlineKeyboardMarkup(volumes)
        await query.message.reply_text("لطفاً میزان حجم درخواستی را انتخاب کنید:", reply_markup=reply_markup)

    # هندلر انتخاب حجم
    if query.data in ["50GB", "100GB", "200GB"]:
        await query.message.reply_text(f"درخواست شما با حجم {query.data} ثبت شد. به زودی با شما تماس خواهیم گرفت.")

# راه‌اندازی ربات
if __name__ == "__main__":
    TOKEN = "7831530422:AAFJwl8Li5mFxmRMLzvGA98zQYu4LB6kGsY"
    app = ApplicationBuilder().token(TOKEN).build()

    # اضافه کردن هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))

    print("ربات شما روشن است!")
    app.run_polling()
