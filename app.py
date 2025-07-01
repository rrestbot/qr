from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import logging

TOKEN = "7643430979:AAFGTjbgWcF073HasxblxP_4ZO3xtvb17fE"
CHANNEL_ID = -1002831436891  # আপনার চ্যানেল ID

# Dictionary to store user info
clicked_users = {}

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton("🔁 Forward this", callback_data='forward_post')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=CHANNEL_ID,
        text="📢 এই পোস্টটি অন্যদের কাছে ফরওয়ার্ড করতে নিচের বাটনে ক্লিক করুন!",
        reply_markup=reply_markup
    )

def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user

    # Store user info
    clicked_users[user.id] = user.username or user.full_name

    # Logging message
    log_msg = f"👤 User clicked forward:\nUsername: @{user.username or 'N/A'}\nName: {user.first_name}\nID: {user.id}"
    context.bot.send_message(chat_id=CHANNEL_ID, text=log_msg)

    query.answer("✅ Thank you for forwarding!")

def stats(update: Update, context: CallbackContext):
    if not clicked_users:
        update.message.reply_text("❌ এখনো কেউ বাটনে ক্লিক করেনি।")
        return

    msg = "📊 Forward Button এ ক্লিক করেছে:\n"
    for uid, uname in clicked_users.items():
        msg += f"🔸 {uname} (ID: {uid})\n"
    update.message.reply_text(msg)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_click))
    dp.add_handler(CommandHandler("stats", stats))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
