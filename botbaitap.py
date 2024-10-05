from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging

# Thông tin bot và admin
BOT_TOKEN = '7623590164:AAEoVKHVYlZ0UcDoKxcPCiSc_FOEAT_tC5s'
ADMIN_CHAT_ID = '6664054279'

# Thông tin tài khoản ngân hàng
ACCOUNT_INFO = """
SỐ Tài Khoản : 9704229203528138715
Chủ tài khoản : DOAN ANH MINH
Ngân Hàng : MB Bank
"""

# Cấu hình logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Hàm bắt đầu với hướng dẫn đầy đủ
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Chào mừng bạn đến với dịch vụ Làm Bài Tập Thuê!\n\n"
        "Hướng dẫn sử dụng các lệnh:\n"
        "/start - Bắt đầu và hiển thị hướng dẫn\n"
        "/stk - Hiển thị thông tin tài khoản thanh toán\n"
        "/website - Truy cập website dịch vụ\n\n"
        "Vui lòng nhập thông tin bài tập của bạn và sau đó gửi ảnh biên lai thanh toán."
    )

# Hàm hiển thị số tài khoản khi người dùng nhập lệnh /stk
def show_account_info(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(ACCOUNT_INFO)

# Hàm tạo nút bấm website khi người dùng nhập lệnh /website
def show_website(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("Truy cập Website", url="https://lixi24.me")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Nhấn vào nút bên dưới để truy cập website:", reply_markup=reply_markup)

# Hàm tiếp nhận tin nhắn văn bản (thông tin bài tập)
def handle_text(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    context.user_data['task_info'] = user_message

    update.message.reply_text(
        "Cảm ơn bạn! Vui lòng gửi ảnh biên lai thanh toán."
    )

# Hàm tiếp nhận ảnh biên lai
def handle_photo(update: Update, context: CallbackContext) -> None:
    photo_file = update.message.photo[-1].get_file()  # Lấy ảnh có độ phân giải cao nhất
    task_info = context.user_data.get('task_info', 'Không có thông tin bài tập')

    # Lấy thông tin user
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    user_info = f"ID: {user_id}" if not username else f"User: @{username} (ID: {user_id})"

    # Gửi thông tin bài tập, user và biên lai tới admin
    caption = f"Thông tin bài tập:\n{task_info}\n\nThông tin người dùng:\n{user_info}"
    context.bot.send_photo(chat_id=ADMIN_CHAT_ID, photo=photo_file.file_id, caption=caption)

    update.message.reply_text(
        "Biên lai của bạn đã được gửi thành công! Chúng tôi sẽ liên hệ lại sớm."
    )

# Hàm xử lý lỗi
def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update "{update}" caused error "{context.error}"')

# Hàm chính để khởi chạy bot
def main() -> None:
    updater = Updater(BOT_TOKEN, use_context=True)

    # Lấy dispatcher để đăng ký các handler
    dispatcher = updater.dispatcher

    # Các lệnh cơ bản
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("stk", show_account_info))  # Lệnh /stk hiển thị thông tin tài khoản
    dispatcher.add_handler(CommandHandler("website", show_website))  # Lệnh /website hiển thị nút bấm tới website

    # Handler cho tin nhắn văn bản và ảnh
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))

    # Log lỗi
    dispatcher.add_error_handler(error)

    # Bắt đầu bot
    updater.start_polling()

    # Chạy bot cho đến khi dừng
    updater.idle()

if __name__ == '__main__':
    main()

