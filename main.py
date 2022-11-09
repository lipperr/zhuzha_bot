import telebot as tb
from telebot import custom_filters, types

TOKEN = '5691379515:AAGNsYkciqoF6IJqjDIfks0GSKJ7FftJY88'

bot = tb.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def hello_message(message):
    bot.send_message(message.chat.id,
                     "Hi there! \n Please type 'options' to see what you can do by clicking once. \n Please type / to "
                     "see quick commands. Commands 'ban', 'unban', 'promote' require you to reply to someone's "
                     "message. Enjoy!")


@bot.message_handler(commands=['ban'])
def ban(message):
    bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)


@bot.message_handler(commands=['unban'])
def unban(message):
    bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)


@bot.message_handler(commands=['promote'])
def promote_myself(message):
    bot.promote_chat_member(message.chat.id, message.reply_to_message.from_user.id, can_change_info=True,
                            can_invite_users=True, can_delete_messages=True,
                            can_restrict_members=True, can_pin_messages=True, can_promote_members=True,
                            can_manage_chat=True, can_manage_video_chats=True, can_manage_voice_chats=True)


@bot.message_handler(content_types=['text'])
def button_message(message):
    if 'options' in message.text:
        markup = types.InlineKeyboardMarkup(row_width=5)
        item_1 = types.InlineKeyboardButton(text="make me admin", callback_data="make me admin")
        markup.row(item_1)
        item_4 = types.InlineKeyboardButton(text="show statistics", callback_data="show statistics")
        markup.row(item_4)
        item_5 = types.InlineKeyboardButton(text="bot, leave this chat", callback_data="bot, leave this chat")
        markup.row(item_5)
        bot.send_message(message.chat.id, 'Choose', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.message:
        if call.data == 'make me admin':
            bot.promote_chat_member(call.message.chat.id, call.from_user.id, can_promote_members=True)
            bot.answer_callback_query(call.id, 'Successful')
        if call.data == 'show statistics':
            num_members = bot.get_chat_members_count(call.message.chat.id)
            admins = len(bot.get_chat_administrators(call.message.chat.id))
            bot.send_message(call.message.chat.id, f"There are {num_members} members and {admins} admins in this chat")
            bot.answer_callback_query(call.id, 'Successful')
        if call.data == 'bot, leave this chat':
            bot.answer_callback_query(call.id, 'Successful')
            bot.leave_chat(call.message.chat.id)


@bot.message_handler(content_types=['new_chat_members'])
def new_member(message):
    user_name = message.new_chat_members[0].first_name
    bot.send_message(message.chat.id, 'hi, {0}!'.format(user_name))


@bot.message_handler(content_types=['left_chat_member'])
def lost_member(message):
    user_name = message.left_chat_member.first_name
    bot.send_message(message.chat.id, 'bye, {0}!'.format(user_name))


if __name__ == '__main__':
    bot.add_custom_filter(custom_filters.TextMatchFilter())
    bot.polling(none_stop=True, interval=0)
