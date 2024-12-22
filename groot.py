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
        keyboard = [
            [InlineKeyboardButton("خرید اکانت جدید", callback_data="buy_account")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("لطفاً گزینه مورد نظر را انتخاب کنید:", reply_markup=reply_markup)
    elif query.data == "buy_account":
        # انتخاب زمان سرویس
        keyboard = [
            [InlineKeyboardButton("1 ماه", callback_data="time_1_month")],
            [InlineKeyboardButton("2 ماه", callback_data="time_2_month")],
            [InlineKeyboardButton("3 ماه", callback_data="time_3_month")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("لطفاً مدت زمان سرویس را انتخاب کنید:", reply_markup=reply_markup)
    elif query.data in ["time_1_month", "time_2_month", "time_3_month"]:
        # ذخیره زمان انتخابی
        context.user_data['time'] = query.data.split('_')[1]  # استخراج زمان (1، 2، 3)
        # انتخاب حجم
        keyboard = [
            [InlineKeyboardButton("10 گیگابایت", callback_data="volume_10")],
            [InlineKeyboardButton("25 گیگابایت", callback_data="volume_25")],
            [InlineKeyboardButton("50 گیگابایت", callback_data="volume_50")],
            [InlineKeyboardButton("75 گیگابایت", callback_data="volume_75")],
            [InlineKeyboardButton("100 گیگابایت", callback_data="volume_100")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("لطفاً حجم اکانت را انتخاب کنید:", reply_markup=reply_markup)
    elif query.data.startswith("volume_"):
        # ذخیره حجم انتخابی
        volume = int(query.data.split('_')[1])
        context.user_data['volume'] = volume

        # محاسبه مبلغ
        time = int(context.user_data['time'])
        price_per_month_per_25gb = 160000  # قیمت به ازای هر 25 گیگ برای یک ماه

        # محاسبه تعداد 25 گیگ برای حجم انتخابی
        total_months = time
        total_volume = volume
        units_of_25gb = (total_volume + 24) // 25  # محاسبه تعداد واحدهای 25 گیگ

        total_price = units_of_25gb * total_months * price_per_month_per_25gb
        # ارسال پیام با مبلغ نهایی
        await query.message.reply_text(f"مبلغ نهایی شما برای {total_volume} گیگابایت و {total_months} ماه سرویس: {total_price} تومان است.")

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
