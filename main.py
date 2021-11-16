import time
import re
import json
import telebot
import random
import requests
from coinbase.wallet.client import Client

coinbase_API_key = "Api key"
coinbase_API_secret = "API secret"

TOKEN = "RS"
AIRDROP = "Nothing"
BOT_TOKEN = "2114816860:AAGVbjslg4BEhRH5z1oN29IGkxQ_ROIOcGo"
PAYMENT_CHANNEL = "@AjayCoder"
OWNER_ID = 1390719325
CHANNELS = ["@EasyCash_offers"]
Mini_Withdraw = 1

botdata = json.load(open('panel.json', 'r'))
admins = botdata['admins']

msg_start = botdata['msgstart']

bot = telebot.TeleBot(BOT_TOKEN)

bonus = {}
withdraw = {}

setbonus_mess = "<b>🟣 Send new bonus amount to set Bonus in bot</b>"
ban_mess = "<b>⚫️ Send user Telegram ID to ban the user</b>"
unban_mess = "<b>🔵 Send user Telegram ID to unban the user</b>"
add_mess = "<b>🟢 Send user Telegram ID to add balance</b>"
cut_mess = "<b>🟡 Send user Telegram ID to cut balance</b>"
setref_mess = "<b>🟠 Send new refer bonus amount to set refer bonus in bot</b>"
setwith_mess = "<b>🔘 Send new minimum withdraw amount to set Minimum withdraw in bot</b>"
addadmin_mess = "<b>🔴 Send new Admin Telegram id to make Admin in bot</b>"
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 

def check(id):
    for i in CHANNELS:
        check = bot.get_chat_member(i, id)
        if check.status != 'left':
            pass
        else:
            return False
    return True

def checkmail(email):
    if(re.search(regex,email)):
        return True
    else:
        return False

def menu(id):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🗃️ Profile')
    keyboard.row('🎁 Bonus', '👥 Referrals','💳 Withdraw')
    keyboard.row('💾 Set Wallet', '📊 Statistics')
    bot.send_message(id, "<b>📋 Menu </b>", parse_mode="html",
                     reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def start(message):
    try:
        user = message.chat.id
        msg = message.text
        if msg == '/start':
            user = str(user)
            data = json.load(open('paytmusers.json', 'r'))
            if user not in data['referred']:
                data['referred'][user] = 0
                data['total'] = data['total'] + 1
            if user not in data['referby']:
                data['referby'][user] = user
            if user not in data['checkin']:
                data['checkin'][user] = 0
            if user not in data['DailyQuiz']:
                data['DailyQuiz'][user] = 0
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            if user not in data['withd']:
                data['withd'][user] = 0
            if user not in data['user']:
                data['user'][user] = 0
            if user not in data['id']:
                data['id'][user] = data['total']+1
            json.dump(data, open('paytmusers.json', 'w'), indent=4)
            time.sleep(0.8)
            print(data)
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(
                text='☑️ Joined ', callback_data='check'))
            bot.send_message(user, msg_start,
                             parse_mode="html", reply_markup=markup)
        else:
            data = json.load(open('paytmusers.json', 'r'))
            user = message.chat.id
            user = str(user)
            refid = message.text.split()[1]
            if user not in data['referred']:
                data['total'] = data['total'] + 1
                data['referred'][user] = 0
            if user not in data['referby']:
                data['referby'][user] = refid
            if user not in data['checkin']:
                data['checkin'][user] = 0
            if user not in data['DailyQuiz']:
                data['DailyQuiz'][user] = 0
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            if user not in data['user']:
                data['user'][user] = 0
            if user not in data['id']:
                data['id'][user] = data['total']+1
            json.dump(data, open('paytmusers.json', 'w'), indent=4)
            time.sleep(0.8)
            ap = json.load(open('panel.json', 'r'))
            msg_tart = str(ap['msgstart'])
            markups = telebot.types.InlineKeyboardMarkup()
            markups.add(telebot.types.InlineKeyboardButton(text='☑️ Joined', callback_data='check'))
            bot.send_message(user, msg_tart,
                             parse_mode="html", reply_markup=markups)
            print(data)
    except:
        bot.send_message(message.chat.id, "An error has been occupied to our server pls wait sometime adn try again")
        return


@bot.message_handler(commands=['panel'])
def panel(message):
    user = str(message.chat.id)
    data = json.load(open('panel.json', 'r'))
    if message.chat.id == OWNER_ID:
        keyboard = [[telebot.types.InlineKeyboardButton('⭕️ Ban user', callback_data='banuser'),
                     telebot.types.InlineKeyboardButton('❕Unban user', callback_data='unbanuser')],
                    [telebot.types.InlineKeyboardButton('➗ Add balance', callback_data='addbalance'),
                     telebot.types.InlineKeyboardButton('🚫 Cut balance', callback_data='cutbalance')],
                    [telebot.types.InlineKeyboardButton(
                        '💲 Add admins', callback_data='addadmins')],
                    [telebot.types.InlineKeyboardButton(
                        '🟡 Set Refer Bonus', callback_data='setrefer')],
                    [telebot.types.InlineKeyboardButton('🟢 Set bonus amount', callback_data='setbonus')]]
        markup8 = telebot.types.InlineKeyboardMarkup(keyboard)
        bot.send_message(message.chat.id, "<b>🔆 Welcome to admin panel</b>",
                         parse_mode="html", reply_markup=markup8)
    elif user not in data['admins']:
        bot.send_message(
            message.chat.id, "<b>You need to become a admin first to open admin panel</b>", parse_mode="html")
    else:
        keyboard = [[telebot.types.InlineKeyboardButton('⭕️ Ban user', callback_data='banuser'),
                     telebot.types.InlineKeyboardButton('❕Unban user', callback_data='unbanuser')],
                    [telebot.types.InlineKeyboardButton('➗ Add balance', callback_data='addbalance'),
                     telebot.types.InlineKeyboardButton('🚫 Cut balance', callback_data='cutbalance')],
                    [telebot.types.InlineKeyboardButton(
                        '💲 Add admins', callback_data='addadmins')],
                    [telebot.types.InlineKeyboardButton(
                        '🟡 Set Refer Bonus', callback_data='setrefer')],
                    [telebot.types.InlineKeyboardButton('🟢 Set bonus amount', callback_data='setbonus')]]
        markup8 = telebot.types.InlineKeyboardMarkup(keyboard)
        bot.send_message(message.chat.id, "<b>🔆 Welcome to admin panel</b>",
                         parse_mode="html", reply_markup=markup8)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
   try:
    ch = check(call.message.chat.id)
    if call.data == 'check':
        if ch == True:
            data = json.load(open('paytmusers.json', 'r'))
            user_id = call.message.chat.id
            user = str(user_id)
            bot.answer_callback_query(
                callback_query_id=call.id, text='✅ You joined.')
            bot.delete_message(call.message.chat.id, call.message.message_id)
            if user not in data['refer']:
                data['refer'][user] = True

                if user not in data['referby']:
                    data['referby'][user] = user
                    json.dump(data, open('paytmusers.json', 'w'),indent=4)
                if int(data['referby'][user]) != user_id:
                    ref_id = int(data['referby'][user])
                    ref = str(ref_id)
                    if ref not in data['balance']:
                        data['balance'][ref] = 0
                    if ref not in data['referred']:
                        data['referred'][ref] = 0
                    time.sleep(0.8)
                    json.dump(data, open('paytmusers.json', 'w'),indent=4)
                    botdata = json.load(open('panel.json', 'r'))
                    Per_Refer = int(botdata['refbonus'])
                    data['balance'][ref] += Per_Refer
                    data['referred'][ref] += 1
                    bot.send_message(
                        ref_id, "<b>☑️New Refer +"+str(Per_Refer)+" "+str(TOKEN)+"</b>", parse_mode="html")
                    json.dump(data, open('paytmusers.json', 'w'),indent=4)
                    return menu(call.message.chat.id)

                else:
                    json.dump(data, open('paytmusers.json', 'w'),indent=4)
                    return menu(call.message.chat.id)

            else:
                json.dump(data, open('paytmusers.json', 'w'),indent=4)
                menu(call.message.chat.id)

        else:
            bot.answer_callback_query(
                callback_query_id=call.id, text='❌ You not Joined')
            bot.delete_message(call.message.chat.id, call.message.message_id)
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton(
                text='☑️ Joined', callback_data='check'))
            bdata = json.load(open('panel.json', 'r'))
            msg_start = bdata['msgstart']
            bot.send_message(call.message.chat.id, msg_start,
                             parse_mode="html", reply_markup=markup)
    if call.data == 'setwallet':
        message = call.message
        user_id = message.chat.id
        user = str(user_id)
        keyboard = telebot.types.ReplyKeyboardMarkup(True)
        keyboard.row('🚫 Cancel')
        send = bot.send_message(message.chat.id, "<b>Enter A Valid Coinbase Email</b>",
                                parse_mode="html", reply_markup=keyboard)
        bot.register_next_step_handler(message, trx_address)
    if call.data == "banuser":
        message = call.message
        bot.send_message(call.message.chat.id, ban_mess, parse_mode="html")
        bot.register_next_step_handler(message, ban)
    if call.data == "unbanuser":
        message = call.message
        bot.send_message(call.message.chat.id, unban_mess,
                         parse_mode="html")
        bot.register_next_step_handler(message, unban)
    if call.data == "addbalance":
        message = call.message
        bot.send_message(call.message.chat.id, add_mess, parse_mode="html")
        bot.register_next_step_handler(message, add_balance)
    if call.data == "cutbalance":
        message = call.message
        bot.send_message(call.message.chat.id, cut_mess, parse_mode="html")
        bot.register_next_step_handler(message, cut_balance)
    if call.data == "setrefer":
        message = call.message
        bot.send_message(call.message.chat.id, setref_mess,
                         parse_mode="html")
        bot.register_next_step_handler(message, set_refer)
    if call.data == "setbonus":
        message = call.message
        bot.send_message(call.message.chat.id, setbonus_mess,
                         parse_mode="html")
        bot.register_next_step_handler(message, set_bonus)
    if call.data == "addadmins":
        message = call.message
        bot.send_message(call.message.chat.id, addadmin_mess,
                         parse_mode="html")
        bot.register_next_step_handler(message, add_admins)
   except:
        bot.send_message(call.message.chat.id, "An error has been occupied to our server pls wait sometime adn try again")
        return


def ban(message):
    try:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        if message.text.isdigit() == False:
            bot.send_message(
                message.chat.id, "<i>📛 Invaild value. Enter only numeric value. Try again</i>", parse_mode="html")
            return
        data = json.load(open('panel.json', 'r'))
        bot.send_message(message.chat.id, "User successfully banned")
        data['banned'].append(message.text)
        json.dump(data, open('panel.json', 'w'), indent=4)
        time.sleep(0.8)
    except:
        bot.send_message(
            message.chat.id, "An error has been occupied to our server pls wait sometime and try again")
        return


def unban(message):
    try:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        if message.text.isdigit() == False:
            bot.send_message(
                message.chat.id, "<i>📛 Invaild value. Enter only numeric value. Try again</i>", parse_mode="html")
            return
        data = json.load(open('panel.json', 'r'))
        bot.send_message(message.chat.id, "User successfully Unbanned")
        data['banned'].remove(message.text)
        json.dump(data, open('panel.json', 'w'), indent=4)
        time.sleep(0.8)
    except:
        bot.send_message(
            message.chat.id, "This user is may not banned if you not sure you can contact our dev @SoulGoku")
        return


def add_balance(message):
    try:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        if message.text.isdigit() == False:
            bot.send_message(
                message.chat.id, "<i>📛 Invaild value. Enter only numeric value. Try again</i>", parse_mode="html")
            return
        data1 = json.load(open('paytmusers.json', 'r'))
        if message.text not in data1['user']:
            bot.send_message(message.chat.id, "This user is not found")
        else:
            data = json.load(open('panel.json', 'r'))
            data['addto'] = message.text
            json.dump(data, open('panel.json', 'w'), indent=4)
            time.sleep(0.8)
            bot.send_message(message.chat.id, "Send amount to add balance")
            bot.register_next_step_handler(message, addbalance)
    except:
        bot.send_message(
            message.chat.id, "An error has been occupied to our server pls wait sometime adn try again")
        return

def cut_balance(message):
    try:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        if message.text.isdigit() == False:
            bot.send_message(
                message.chat.id, "<i>📛 Invaild value. Enter only numeric value. Try again</i>", parse_mode="html")
            return
        data1 = json.load(open('paytmusers.json', 'r'))
        if message.text not in data1['user']:
            bot.send_message(message.chat.id, "This user is not found")
        else:
            data = json.load(open('panel.json', 'r'))
            data['addto'] = message.text
            json.dump(data, open('panel.json', 'w'), indent=4)
            time.sleep(0.8)
            bot.send_message(message.chat.id, "Send amount to cut balance")
            bot.register_next_step_handler(message, cutbalance)
    except:
        bot.send_message(
            message.chat.id, "An error has been occupied to our server pls wait sometime and try again")
        return


def addbalance(message):
    try:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        if message.text.isdigit() == False:
            bot.send_message(
                message.chat.id, "<i>📛 Invaild value. Enter only numeric value. Try again</i>", parse_mode="html")
            return
        data2 = json.load(open('panel.json', 'r'))
        bot.send_message(message.chat.id, "Added successfully")
        data = json.load(open('paytmusers.json', 'r'))
        data['balance'][data2['addto']] += int(message.text)
        json.dump(data, open('paytmusers.json', 'w'), indent=4)
        time.sleep(0.8)
    except:
        bot.send_message(
            message.chat.id, "An error has been occupied to our server pls wait sometime adn try again")
        return


def cutbalance(message):
    try:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        if message.text.isdigit() == False:
            bot.send_message(
                message.chat.id, "<i>📛 Invaild value. Enter only numeric value. Try again</i>", parse_mode="html")
            return
        data2 = json.load(open('panel.json', 'r'))
        bot.send_message(message.chat.id, "Added successfully")
        data = json.load(open('paytmusers.json', 'r'))
        data['balance'][data2['addto']] -= int(message.text)
        json.dump(data, open('paytmusers.json', 'w'), indent=4)
        time.sleep(0.8)
    except:
        bot.send_message(
            message.chat.id, "An error has been occupied to our server pls wait sometime adn try again")
        return


def set_bonus(message):
    try:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        if message.text.isdigit() == False:
            bot.send_message(
                message.chat.id, "<i>📛 Invaild value. Enter only numeric value. Try again</i>", parse_mode="html")
            return
        data = json.load(open('panel.json', 'r'))
        bot.send_message(
            message.chat.id, "New bonus amount is set successfully")
        data['bonus'] = int(message.text)
        json.dump(data, open('panel.json', 'w'), indent=4)
        time.sleep(0.8)
    except:
        bot.send_message(
            message.chat.id, "An error has been occupied to our server pls wait sometime and try again")
        return


def set_refer(message):
    try:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        if message.text.isdigit() == False:
            bot.send_message(
                message.chat.id, "<i>📛 Invaild value. Enter only numeric value. Try again</i>", parse_mode="html")
            return
        data = json.load(open('panel.json', 'r'))
        bot.send_message(
            message.chat.id, "New refer bonus amount is set successfully")
        data['refbonus'] = int(message.text)
        json.dump(data, open('panel.json', 'w'), indent=4)
        time.sleep(0.8)
    except:
        bot.send_message(
            message.chat.id, "An error has been occupied to our server pls wait sometime and try again")
        return


def add_admins(message):
    try:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        if message.text.isdigit() == False:
            bot.send_message(
                message.chat.id, "<i>📛 Invaild value. Enter only numeric value. Try again</i>", parse_mode="html")
            return
        data = json.load(open('panel.json', 'r'))
        bot.send_message(
            message.chat.id, "Admin successfully added You can remove it by editing panel.json file in your server")
        data['admins'].append(message.text)
        json.dump(data, open('panel.json', 'w'), indent=4)
        time.sleep(0.8)
    except:
        bot.send_message(
            message.chat.id, "An error has been occupied to our server pls wait sometime and try again")
        return


@bot.message_handler(content_types=['text'])
def send_text(message):
   try:
      ch = check(message.chat.id)
      if ch == True:
        if message.chat.id == OWNER_ID:
            if message.text == '/addu':
                bot.send_message(OWNER_ID, "Send User ID to add balance")
                bot.register_next_step_handler(message, add_balance)
        if message.text == '🗃️ Profile':
            data = json.load(open('paytmusers.json', 'r'))
            accmsg = '<b>👮 User : {}\n\n💾 Wallet : </b><code>{}</code><b>\n\n💸 Balance : </b><code>{}</code><b> {}</b>'
            user_id = message.chat.id
            user = str(user_id)

            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"

            json.dump(data, open('paytmusers.json', 'w'), indent=4)
            time.sleep(0.8)
            balance = data['balance'][user]
            wallet = data['wallet'][user]
            msg = accmsg.format(message.from_user.first_name,
                                wallet, balance, TOKEN)
            bot.send_message(message.chat.id, msg, parse_mode="html")

        if message.text == '👥 Referrals':
            data = json.load(open('paytmusers.json', 'r'))
            bot_name = bot.get_me().username
            user_id = message.chat.id
            user = str(user_id)
            botdata = json.load(open('panel.json', 'r'))
            Per_Refer = int(botdata['refbonus'])
            if user not in data['referred']:
                data['referred'][user] = 0
            json.dump(data, open('paytmusers.json', 'w'), indent=4)
            time.sleep(0.8)
            ref_count = data['referred'][user]
            ref_link = 'https://t.me/'+str(bot_name)+'?start='+str(message.chat.id)
            ref_msg = "<b>⏯️ Total Invites : "+str(ref_count)+" Users\n\n👥 Refferrals System\n\n🙇 Per Refer :-  "+str(Per_Refer)+" "+str(TOKEN)+"\n\n🔗 Referral Link ⬇️\n"+str(ref_link)+"</b>"
            bot.send_message(message.chat.id, ref_msg, parse_mode="html")
        if message.text == "💾 Set Wallet":
            user_id = message.chat.id
            user = str(user_id)

            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            keyboard.row('🚫 Cancel')
            send = bot.send_message(message.chat.id, "<b>Enter A Valid Coinbase Email</b>",
                                    parse_mode="html", reply_markup=keyboard)
            bot.register_next_step_handler(message, trx_address)
        if message.text == "🎁 Bonus":
            botdata = json.load(open('panel.json', 'r'))
            Daily_bonus = int(botdata['bonus'])
            user_id = message.chat.id
            user = str(user_id)
            cur_time = int((time.time()))
            data = json.load(open('paytmusers.json', 'r'))
            if (user_id not in bonus.keys()) or (cur_time - bonus[user_id] > 24*60*60):
                data['balance'][(user)] += int(Daily_bonus)
                bot.send_message(
                    user_id, "<b>Congrats you just received "+str(Daily_bonus)+" Paytm CASH</b>", parse_mode="html")
                bonus[user_id] = cur_time
                json.dump(data, open('paytmusers.json', 'w'), indent=4)
                time.sleep(0.8)
            else:
                bot.send_message(
                    message.chat.id, "<b>❌You can only take bonus once every 24 hours!</b>", parse_mode="html")
            return

        if message.text == "📊 Statistics":
            user_id = message.chat.id
            user = str(user_id)
            data = json.load(open('paytmusers.json', 'r'))
            msg = "<b>📊 Total members : {} Users\n\n💎 Total successful Withdraw : {} {}</b>"
            msg = msg.format(data['total'], data['totalwith'], TOKEN)
            bot.send_message(user_id, msg, parse_mode="html")
            return
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        if message.text == "💳 Withdraw":
            user_id = message.chat.id
            user = str(user_id)

            data = json.load(open('paytmusers.json', 'r'))
            cur_time = int((time.time()))
            if (user_id not in withdraw.keys()) or (cur_time - withdraw[user_id] > 60):
                if user not in data['balance']:
                    data['balance'][user] = 0
                if user not in data['wallet']:
                    data['wallet'][user] = "none"
                json.dump(data, open('paytmusers.json', 'w'), indent=4)
                time.sleep(0.8)
                bal = data['balance'][user]
                wall = data['wallet'][user]
                if wall == "none":
                    markup = telebot.types.InlineKeyboardMarkup()
                    markup.add(telebot.types.InlineKeyboardButton(
                        text='✅ Set wallet', callback_data='setwallet'))
                    bot.send_message(user_id, "<b>⚠️ Your Wallet is</b> <code>Not set</code>\n‼️ <b>Please set your wallet first For withdraw</b>",
                                     parse_mode="html", reply_markup=markup)
                    return
                if bal >= Mini_Withdraw:
                    bot.send_message(user_id, "<b>Enter amount to withdraw Your "+str(TOKEN)+"\n\nCurrent wallet: "+wall+"</b>",
                                     parse_mode="html")
                    bot.register_next_step_handler(message, amo_with)
                else:
                    bot.send_message(
                        user_id, "<i>❌ Your balance low you should have at least "+str(Mini_Withdraw)+" "+str(TOKEN)+" to Withdraw</i>", parse_mode="html")
                    return
            else:
                bot.send_message(
                    message.chat.id, "<b>❌ You can do only 1 withdraw in 24 hours!</b>", parse_mode="html")
                return
      else:
        markups = telebot.types.InlineKeyboardMarkup()
        markups.add(telebot.types.InlineKeyboardButton(text='☑️ Joined', callback_data='check'))
        bdata = json.load(open('panel.json', 'r'))
        msg_start = bdata['msgstart']
        bot.send_message(message.chat.id, msg_start,parse_mode="html", reply_markup=markups)
   except:
      bot.send_message(
          message.chat.id, "An error has been occupied to our server pls wait sometime adn try again")
      return 

def trx_address(message):
   try:
      ch = check(message.chat.id)
      if ch == True:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        if checkmail(message.text) == True:
            user_id = message.chat.id
            user = str(user_id)
            data = json.load(open('paytmusers.json', 'r'))
            data['wallet'][user] = message.text

            bot.send_message(message.chat.id, "<b>💹 Your Coinbase Email set to " +
                             data['wallet'][user]+"</b>", parse_mode="html")
            json.dump(data, open('paytmusers.json', 'w'), indent=4)
            time.sleep(0.8)
            return menu(message.chat.id)
        else:
            bot.send_message(
                message.chat.id, "<b>⚠️ It's Not a Valid Email!</b>", parse_mode="html")
            return menu(message.chat.id)
      else:
        markups = telebot.types.InlineKeyboardMarkup()
        markups.add(telebot.types.InlineKeyboardButton(text='☑️ Joined', callback_data='check'))
        bdata = json.load(open('panel.json', 'r'))
        msg_start = bdata['msgstart']
        bot.send_message(message.chat.id, msg_start,parse_mode="html", reply_markup=markups)
   except:
        bot.send_message(
            message.chat.id, "An error has been occupied to our server pls wait sometime adn try again")
        return


def amo_with(message):
   #try:
      ch = check(message.chat.id)
      if ch == True:
        if message.text == "🚫 Cancel":
            return menu(message.chat.id)
        data = json.load(open('panel.json', 'r'))
        if message.chat.id not in data['banned']:
            user_id = message.chat.id
            amo = message.text
            user = str(user_id)
            h = message.text.replace(".","")
            data = json.load(open('paytmusers.json', 'r'))
            if h.isdigit() == True:
                pass
            else:
                bot.send_message(user_id, "Please Choose a valid amount")
                bot.register_next_step_handler(message, amo_with)
                return
            if user not in data['balance']:
                data['balance'][user] = 0
            if user not in data['wallet']:
                data['wallet'][user] = "none"
            json.dump(data, open('paytmusers.json', 'w'), indent=4)
            time.sleep(0.8)
            bal = data['balance'][user]
            wall = data['wallet'][user]
            msg = message.text
            amo = float(amo)
            if float(amo) > bal:
                bot.send_message(
                    user_id, "<i>❌ You Can't withdraw More than Your Balance</i>", parse_mode="html")
                return menu(message.chat.id)
            client = Client(coinbase_API_key, coinbase_API_secret)
            tx = client.send_money('815cc264-102e-56f3-9de4-32a2fa13b165',
                       to=wall,
                       amount=message.text,
                       currency='LTC',
                       idem='9316dd16-0c05')
            print(tx)
            asd = tx.off_chain_status
            if asd == "completed":
                data['withd'][user] += 1
                data['balance'][user] -= float(amo)
                data['totalwith'] += float(amo)
                json.dump(data, open('paytmusers.json', 'w'))
                time.sleep(0.8)
                cur_time2 = int((time.time()))
                withdraw[user_id] = cur_time2
                bot.send_message(message.chat.id, "<b>🎉 Withdraw Success ✅\n\n😎 User : "+str(message.chat.id)+"\n📧 Email : "+str(wall)+"\n💰 Amount : "+str(message.text)+" "+str(TOKEN)+"\n\n🕹 In Bot : @"+str(bot.get_me().username)+"</b>",parse_mode="html")
                bot.send_message(PAYMENT_CHANNEL, "<b>🎉 Withdraw Success ✅\n\n😎 User : "+str(message.chat.id)+"\n📧 Email : "+str(wall)+"\n💰 Amount : "+str(message.text)+" "+str(TOKEN)+"\n\n🕹 In Bot : @"+str(bot.get_me().username)+"</b>",parse_mode="html")
                return menu(message.chat.id)
            else:
                bot.send_message(
                    user_id, "Something Goes wrong please check your wallet is correct and then come back later.")
                return menu(message.chat.id)
        else:
            bot.send_message(message.chat.id, "Sorry you are banned")
      else:
        markups = telebot.types.InlineKeyboardMarkup()
        markups.add(telebot.types.InlineKeyboardButton(text='☑️ Joined', callback_data='check'))
        bdata = json.load(open('panel.json', 'r'))
        msg_start = bdata['msgstart']
        bot.send_message(message.chat.id, msg_start,parse_mode="html", reply_markup=markups)
#   except:
 #       bot.send_message(user_id, "Something Goes wrong please check your wallet is correct and then come back later.")
  #      return


if __name__ == '__main__':
    bot.polling(none_stop=True)

