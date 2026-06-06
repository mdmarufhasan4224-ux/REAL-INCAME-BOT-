from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# ====================================
# BOT SETTINGS
# ====================================

TOKEN = "8921142309:AAF_kYR291USCCmgWcl23JJIUqSPXtNdZbY"

CHANNEL_USERNAME = "@REALCOMEBD"

BOT_USERNAME = "REALINCAMEBOT_bot"

ADMIN_ID = 8253107257

# ====================================
# DATABASE
# ====================================

balances = {}
refer_balances = {}
user_uid = {}
withdraw_type = {}
task_step = {}

# ====================================
# MAIN MENU
# ====================================

main_menu = ReplyKeyboardMarkup(
    [
        ["✨ TASK", "🤖 BOT REFER"],
        ["👤 PROFILE", "💰 BALANCE"],
        ["☎ SUPPORT"]
    ],
    resize_keyboard=True
)

# ====================================
# START COMMAND
# ====================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    user_id = user.id

    if user_id not in balances:
        balances[user_id] = 0

    if user_id not in refer_balances:
        refer_balances[user_id] = 0

    if user_id not in task_step:
        task_step[user_id] = 1

    # ====================================
    # REFERRAL SYSTEM
    # ====================================

    if context.args:

        try:

            referrer = int(context.args[0])

            if referrer != user_id:

                refer_balances[referrer] += 0.20

                await context.bot.send_message(
                    chat_id=referrer,
                    text="""
🎉 নতুন একজন user আপনার referral link দিয়ে join করেছে

💸 ০.২০ টাকা যোগ হয়েছে
"""
                )

        except:
            pass

    buttons = [

        [
            InlineKeyboardButton(
                "📢 JOIN CHANNEL",
                url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"
            )
        ],

        [
            InlineKeyboardButton(
                "✅ I HAVE JOINED",
                callback_data="joined"
            )
        ]

    ]

    await update.message.reply_text(
        "📢 প্রথমে channel join করুন",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ====================================
# JOIN CHECK
# ====================================

async def joined(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    user = query.from_user

    try:

        member = await context.bot.get_chat_member(
            CHANNEL_USERNAME,
            user.id
        )

        if member.status in [
            "member",
            "administrator",
            "creator"
        ]:

            await query.message.delete()

            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"👋 Welcome {user.first_name}",
                reply_markup=main_menu
            )

        else:

            await query.answer(
                "❌ আগে channel join করুন",
                show_alert=True
            )

    except:

        await query.answer(
            "❌ আগে channel join করুন",
            show_alert=True
        )

# ====================================
# BUTTON HANDLER
# ====================================

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    user_id = user.id
    text = update.message.text

    # ====================================
    # TASK
    # ====================================

    if text == "✨ TASK":

        task_step[user_id] = 1

        msg = """
📝 CURRENT AVAILABLE TASK

━━━━━━━━━━━━━━━

💸 1 TASK — 10 TK

📌 নিচের button এ চাপ দিন

✅ কাজ করার পরে:

• Screenshot পাঠান
• UID পাঠান

━━━━━━━━━━━━━━━

⚠️ Screenshot + UID ছাড়া balance add হবে না।

Games are better with friends! Come join me in Gemgala. 👯
https://getblock.me/u/24757057
"""

        buttons = [
            [
                InlineKeyboardButton(
                    "🔗 TASK HERE",
                    url="https://getblock.me/u/24757057"
                )
            ]
        ]

        await update.message.reply_text(
            msg,
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True
        )

    # ====================================
    # NEXT TASK
    # ====================================

    elif text == "➡ NEXT TASK":

        if task_step.get(user_id, 1) == 1:

            task_step[user_id] = 2

            msg = """
📝 CURRENT AVAILABLE TASK

━━━━━━━━━━━━━━━

💸 2 TASK — 10 TK

📌 নিচের button এ চাপ দিন

✅ কাজ করার পরে:

• Screenshot পাঠান
• UID পাঠান

━━━━━━━━━━━━━━━

⚠️ Screenshot + UID ছাড়া balance add হবে না।

Games are better with friends! Come join me in Gemgala. 👯
https://getblock.me/u/48373744
"""

            buttons = [
                [
                    InlineKeyboardButton(
                        "🔗 TASK HERE",
                        url="https://getblock.me/u/48373744"
                    )
                ]
            ]

            await update.message.reply_text(
                msg,
                reply_markup=InlineKeyboardMarkup(buttons),
                disable_web_page_preview=True
            )

        else:

            cancel_btn = ReplyKeyboardMarkup(
                [
                    ["❌ CANCEL"]
                ],
                resize_keyboard=True
            )

            await update.message.reply_text(
                """
❌ এই মুহূর্তে আমাদের কাছে আর কোনো কাজ নেই।

⏳ দয়া করে অপেক্ষা করেন।
নতুন কাজ এড করা হবে।

ধন্যবাদ ❤️
""",
                reply_markup=cancel_btn
            )

    # ====================================
    # PROFILE
    # ====================================

    elif text == "👤 PROFILE":

        task_balance = balances.get(user_id, 0)
        refer_balance = refer_balances.get(user_id, 0)

        msg = f"""
👤 PROFILE

━━━━━━━━━━━━━━━

🆔 User ID : {user_id}

💸 Task Balance : {task_balance} TK

🤖 Refer Balance : {refer_balance:.2f} TK
"""

        await update.message.reply_text(msg)

    # ====================================
    # BALANCE
    # ====================================

    elif text == "💰 BALANCE":

        task_balance = balances.get(user_id, 0)
        refer_balance = refer_balances.get(user_id, 0)

        total = task_balance + refer_balance

        withdraw_btn = ReplyKeyboardMarkup(
            [
                ["💳 WITHDRAW"],
                ["❌ CANCEL"]
            ],
            resize_keyboard=True
        )

        msg = f"""
💰 YOUR BALANCE

━━━━━━━━━━━━━━━

💸 Task Balance : {task_balance} TK

🤖 Refer Balance : {refer_balance:.2f} TK

🟢 Total Balance : {total:.2f} TK
"""

        await update.message.reply_text(
            msg,
            reply_markup=withdraw_btn
        )

    # ====================================
    # CANCEL
    # ====================================

    elif text == "❌ CANCEL":

        await update.message.reply_text(
            "❌ Cancel Done",
            reply_markup=main_menu
        )

    # ====================================
    # WITHDRAW
    # ====================================

    elif text == "💳 WITHDRAW":

        withdraw_menu = ReplyKeyboardMarkup(
            [
                ["💸 TASK WITHDRAW"],
                ["🤖 REFER WITHDRAW"],
                ["❌ CANCEL"]
            ],
            resize_keyboard=True
        )

        await update.message.reply_text(
            "💳 কোন balance withdraw করবেন?",
            reply_markup=withdraw_menu
        )

    # ====================================
    # TASK WITHDRAW
    # ====================================

    elif text == "💸 TASK WITHDRAW":

        if balances.get(user_id, 0) <= 0:

            await update.message.reply_text(
                "❌ আপনার Task Balance নেই"
            )

            return

        withdraw_type[user_id] = "task"

        await update.message.reply_text(
            "📲 আপনার BKash নাম্বার দিন"
        )

    # ====================================
    # REFER WITHDRAW
    # ====================================

    elif text == "🤖 REFER WITHDRAW":

        if refer_balances.get(user_id, 0) < 20:

            await update.message.reply_text(
                "❌ Refer Balance ২০ টাকা হয়নি"
            )

            return

        withdraw_type[user_id] = "refer"

        await update.message.reply_text(
            "📲 আপনার BKash নাম্বার দিন"
        )

    # ====================================
    # BKASH NUMBER
    # ====================================

    elif text.startswith("01") and len(text) == 11:

        if user_id not in withdraw_type:
            return

        wtype = withdraw_type[user_id]

        if wtype == "task":
            amount = balances[user_id]
        else:
            amount = refer_balances[user_id]

        admin_text = f"""
💳 NEW WITHDRAW REQUEST

👤 Name : {user.first_name}

🆔 User ID : {user_id}

💰 Amount : {amount} TK

📲 BKash : {text}

📌 Type : {wtype}
"""

        buttons = [
            [
                InlineKeyboardButton(
                    "✅ PAYMENT SENT",
                    callback_data=f"paid_{user_id}_{wtype}"
                )
            ]
        ]

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

        await update.message.reply_text(
            """
✅ আপনার withdraw request জমা হয়েছে

Admin approve করলে টাকা পাবেন।
"""
        )

    # ====================================
    # BOT REFER
    # ====================================

    elif text == "🤖 BOT REFER":

        refer_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"

        msg = f"""
💸 প্রতি রেফারে ০.২০ টাকা পাবেন

━━━━━━━━━━━━━━━

🔗 YOUR REFER LINK 👇

{refer_link}

━━━━━━━━━━━━━━━

📢 বন্ধুদের share করুন এবং income করুন।
"""

        await update.message.reply_text(
            msg,
            disable_web_page_preview=True
        )

    # ====================================
    # SUPPORT
    # ====================================

    elif text == "☎ SUPPORT":

        await update.message.reply_text(
            """
☎ SUPPORT

👨‍💻 Admin :
@MARUFOWNER0
"""
        )

    # ====================================
    # UID SAVE
    # ====================================

    elif text.isdigit():

        user_uid[user_id] = text

        await update.message.reply_text(
            "📸 এখন Screenshot পাঠান"
        )

# ====================================
# PHOTO HANDLER
# ====================================

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    user_id = user.id

    if user_id not in user_uid:
        return

    uid = user_uid[user_id]

    photo = update.message.photo[-1].file_id

    buttons = [
        [
            InlineKeyboardButton(
                "✅ APPROVE",
                callback_data=f"approve_{user_id}"
            ),

            InlineKeyboardButton(
                "❌ REJECT",
                callback_data=f"reject_{user_id}"
            )
        ]
    ]

    caption = f"""
📥 NEW TASK SUBMISSION

👤 Name : {user.first_name}

🆔 User ID : {user_id}

📌 UID : {uid}
"""

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

    next_btn = ReplyKeyboardMarkup(
        [
            ["➡ NEXT TASK"],
            ["❌ CANCEL"]
        ],
        resize_keyboard=True
    )

    await update.message.reply_text(
        """
✅ আপনার কাজ জমা দেওয়া হয়েছে

Admin approve করলে আপনার balance টাকা এড হবে।
""",
        reply_markup=next_btn
    )

# ====================================
# ADMIN BUTTONS
# ====================================

async def admin_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    data = query.data

    # ====================================
    # APPROVE
    # ====================================

    if data.startswith("approve_"):

        user_id = int(data.split("_")[1])

        balances[user_id] += 10

        await context.bot.send_message(
            chat_id=user_id,
            text="""
🎉 আপনার task approve হয়েছে

💰 10 টাকা balance এ যোগ হয়েছে।
"""
        )

        await query.answer("Approved")

    # ====================================
    # REJECT
    # ====================================

    elif data.startswith("reject_"):

        user_id = int(data.split("_")[1])

        await context.bot.send_message(
            chat_id=user_id,
            text="""
❌ আপনার task reject হয়েছে
"""
        )

        await query.answer("Rejected")

    # ====================================
    # PAYMENT SENT
    # ====================================

    elif data.startswith("paid_"):

        split_data = data.split("_")

        user_id = int(split_data[1])
        wtype = split_data[2]

        if wtype == "task":
            balances[user_id] = 0
        else:
            refer_balances[user_id] = 0

        await context.bot.send_message(
            chat_id=user_id,
            text="""
✅ আপনার payment পাঠানো হয়েছে
"""
        )

        await query.answer("Payment Sent")

# ====================================
# MAIN
# ====================================

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    CallbackQueryHandler(
        joined,
        pattern="joined"
    )
)

app.add_handler(
    CallbackQueryHandler(
        admin_buttons,
        pattern="approve_|reject_|paid_"
    )
)

app.add_handler(
    MessageHandler(
        filters.PHOTO,
        photo_handler
    )
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        buttons
    )
)

print("✅ BOT RUNNING SUCCESSFULLY")

app.run_polling()
