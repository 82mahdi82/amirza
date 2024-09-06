import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton,WebAppInfo
from text import robot_text
import database
import utils

database.CreateDatabase()
database.CreateTable()
TOKEN = '7300074403:AAFwYTRXj8c9iib72mrOF5UcVfgxqKE5P4I' #'7018847010:AAEMTrqs7mZRwxyaXE_XUgbyYPYzl_Twt3M' 

admin = 193483410 #748626808
channel_text = -1002236629948

userStep={}
dict_new_letters = {} # cid : letters
dict_word = {}  # letters : [word1, word2, ...]

dict_edit_letters = {} # level : 2, letters : abc, words: []
dict_add_word = {}
dict_cid_class = {}  # cid : class

dict_plan_information = {}
dict_shop_information = {}

dict_adv = {}
rezerv_adv = []
dict_user_adv = {}
 
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        cid = m.chat.id
        if m.content_type == 'text':
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + m.text)
        elif m.content_type == 'photo':
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + "New photo recieved")
        elif m.content_type == 'document':
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + 'New Document recieved')


bot = telebot.TeleBot(TOKEN,num_threads=3)
bot.set_update_listener(listener)

#-----------------------------------------------------------------def----------------------------------------------------------
def is_user_member(user_id, channel_id):
    try:
        chat_member = bot.get_chat_member(channel_id, user_id)
        return chat_member.status == "member" or chat_member.status == "administrator" or chat_member.status == "creator"
    except Exception as e:
        return False

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        userStep[uid] = 0
        return 0

def markup_config_admin():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(robot_text['word'], callback_data= 'admin_word')) 
    markup.add(InlineKeyboardButton(robot_text['manage_word'], callback_data= 'admin_manageword')) 
    markup.add(InlineKeyboardButton('آمار',callback_data='admin_amar'))
    markup.add(InlineKeyboardButton('ارسال همگانی',callback_data='admin_brodcast'),InlineKeyboardButton('فوروارد همگانی',callback_data='admin_forall'))
    markup.add(InlineKeyboardButton('افزودن کانال تبلیغاتی', callback_data='admin_adv'))
    markup.add(InlineKeyboardButton('حذف کانال های تبلیغاتی', callback_data='deleteadv'))
    return markup

def reply_markup_main():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(robot_text['game'])
    markup.add(robot_text['best'], robot_text['buy'])
    markup.add(robot_text['shop'], robot_text['tabligh'])
    markup.add(robot_text['invite'])

    # markup.add(robot_text['game'])
    return markup


def can_form_word(word, letters):
    list_letters = list(letters)
    word_no_space = word.replace(' ','')

    for char in word_no_space:
        if char in list_letters:
            list_letters.remove(char)
        else:
            return False
    return True

def get_level():
    list_dict_letters = database.select_letters()
    level = 0
    if len(list_dict_letters) > 0:
        for letter in list_dict_letters:
            if letter['level'] > level:
                 level = letter['level'] 
        level += 1
    return level

def get_number_word(word):
    word_not_space = word.replace(' ','')
    if len(word_not_space) == 2:
        return 'دو حرفی'
    elif len(word_not_space) == 3:
        return 'سه حرفی'
    elif len(word_not_space) == 4:
        return 'چهار حرفی'
    elif len(word_not_space) == 5:
        return 'پنج حرفی'
    elif len(word_not_space) == 6:
        return 'شش حرفی'
    elif len(word_not_space) == 7:
        return 'هفت حرفی'
    elif len(word_not_space) == 8:
        return 'هشت حرفی'


def get_text_game(cid):
    instans_game = dict_cid_class[cid]
    words = database.select_words(instans_game.level)
    info_user = database.select_user(cid)[0]
    text = ''
    text += f'لول {info_user["level"]} ⚜\n'
    text += f'موجودی {info_user["inventory"]} سکه 🪙\n'
    text += '➖➖➖➖➖➖➖➖➖➖➖➖\n'
    text += f'مرحله {instans_game.level}\n'
    text += 'کلمات : \n'
    for word in words:
        kalame = ''
        for index ,harf in enumerate(list(word['word'])):
            if harf == ' ':
                kalame += ' '
            # elif word['word'] in instans_game.dict_hint:
            #     if index in  instans_game.dict_hint[word['word']]:
            #         kalame += instans_game.dict_hint[word['word']][index]
            #     else:
            #        kalame += '❔' 
            else:
                kalame += '❔'
        if instans_game.is_word_selected(word['word']):
            if len(instans_game.selected_letters) > 0:
                list_kalame = list(kalame)
                print(list_kalame)
                print('instans_game.selected_letters', instans_game.selected_letters)
                index = 0
                for i in range(len(list_kalame)):
                    if list_kalame[i] == '❔' and instans_game.selected_letters[index] != None:
                        list_kalame[i] = instans_game.letters[instans_game.selected_letters[index]]
                    index += 1
                print(list_kalame)
                text_kalame = ''.join(list_kalame)
                text += f'✅ {get_number_word(word["word"])}: {text_kalame}\n'
            else:
                text += f'✅ {get_number_word(word["word"])}: {kalame}\n'
        elif instans_game.is_completed(word['word']):
            text += f'{get_number_word(word["word"])}: {word["word"]} 🥳\n'
        else:
            text += f'{get_number_word(word["word"])}: {kalame}\n'

    return text


def show_number_words(cid):
    info_user = database.select_user(cid)[0]
    words = database.select_words(info_user['level'])
    markup = InlineKeyboardMarkup()
    list_markup = []
    for word in words:
        word_not_space = word['word'].replace(' ','')
        number_text = get_number_word(word['word'])
        if dict_cid_class[cid].is_completed(word['word']):
            list_markup.append(InlineKeyboardButton(number_text + " 🥳", callback_data = f'wordselect_completed'))
        elif dict_cid_class[cid].is_word_selected(word['word']):
            list_markup.append(InlineKeyboardButton(number_text + " ✅", callback_data = f'wordselect_selected'))
        else:
            list_markup.append(InlineKeyboardButton(number_text, callback_data = f'wordselect_{info_user["level"]}_{word["word"]}'))
    markup.add(*list_markup)


    list_markup2 = []
    
    dict_letters = dict_cid_class[cid].letters
    print('dict_letters',dict_letters)
    for id_letter in dict_letters:
        if dict_cid_class[cid].is_letter_selected(id_letter):
            list_markup2.append(InlineKeyboardButton(dict_letters[id_letter] + " ✅", callback_data = f'letterselect_selected'))
        # elif dict_cid_class[cid].check_letter_in_hint(dict_letters[id_letter]):
        #     list_markup2.append(InlineKeyboardButton(dict_letters[id_letter] + " ✅", callback_data = f'letterselect_selected'))
        else:
            list_markup2.append(InlineKeyboardButton(dict_letters[id_letter], callback_data = f'letterselect_{id_letter}_{dict_cid_class[cid].level}'))
    markup.add(*list_markup2)

    markup.add(InlineKeyboardButton('راهنمایی | 90 سکه 🪙', callback_data=f'hint_{dict_cid_class[cid].level}'))
    markup.add(InlineKeyboardButton('بازیابی', callback_data=f'bazyabi_{info_user["level"]}'))
    return markup


def msg_game(m):
    cid = m.chat.id
    mid = m.message_id
    bot.edit_message_text(get_text_game(cid), cid, mid,reply_markup=show_number_words(cid) )
# 🎮 ⚜ 🪙 💳 📊 ↪


def markup_buy():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('2500 سکه 🪙 | قیمت 💳 10 تومن', callback_data='buy_10_2500'))
    markup.add(InlineKeyboardButton('10000 سکه 🪙 | قیمت 💳 30 تومن', callback_data='buy_30_10000'))
    markup.add(InlineKeyboardButton('50000 سکه 🪙 | قیمت 💳 100 تومن', callback_data='buy_100_50000'))
    return markup

def shop_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('2500 سکه 🪙 | 1 استارز', callback_data='shop_1_2500'))
    markup.add(InlineKeyboardButton('10000 سکه 🪙 | 3 استارز', callback_data='shop_3_10000'))
    markup.add(InlineKeyboardButton('50000 سکه 🪙 | 10 استارز', callback_data='shop_10_50000'))
    return markup

#------------------------------------------------------commands-------------------------------------------------
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    print(m.from_user)
    bot.copy_message(cid, channel_text, 12,reply_markup= reply_markup_main())
    if cid == admin:
        database.insert_user(cid, m.from_user.first_name)
        bot.send_message(cid, "ادمین گرامی برای  تنظیمات ربات از دستور /config استفاده کنید")

    if m.text.endswith('start') == False:
        check_cid = database.select_user(cid)
        if check_cid == []:
            database.insert_user(cid, m.from_user.first_name)
            uid = int(m.text.split(' ')[1])
            check = database.select_user(uid)
            if len(check) > 0:
                info_user = check[0]
                database.update_user(info_user['inventory']+400, uid)
                bot.send_message(uid ,robot_text['invite_msg_user'].format(m.from_user.first_name))
    
    database.insert_user(cid, m.from_user.first_name)

@bot.message_handler(commands=['config'])
def command_start(m):
    cid = m.chat.id
    if cid == admin:
        bot.copy_message(cid, channel_text, 2, reply_markup=markup_config_admin())

    

#---------------------------------------------------callback------------------------------------------------------------    
@bot.callback_query_handler(func=lambda call: call.data.startswith("deleteadv"))
def call_callback_panel_sends(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data.split("_")  
    if len(data) > 1:
        database.delete_adv(int(data[1]))
        list_adv = database.select_adv()
        if len(list_adv) > 0:
            markup = InlineKeyboardMarkup()
            for adv in list_adv:
                markup.add(InlineKeyboardButton(adv['title'], callback_data=f'deleteadv_{adv["channel_id"]}'))
            markup.add(InlineKeyboardButton(robot_text['back'], callback_data = 'admin_back_main'))
            bot.edit_message_text('برای حذف کانال مورد نظر بر روی آن کلیک کنید',cid, mid, reply_markup=markup)
        else:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(robot_text['back'], callback_data = 'admin_back_main'))
            bot.edit_message_text('تمامی کانال ها حذف شدند',cid, mid,reply_markup=markup)

    else:
        list_adv = database.select_adv()
        if len(list_adv) > 0:
            markup = InlineKeyboardMarkup()
            for adv in list_adv:
                markup.add(InlineKeyboardButton(adv['title'], callback_data=f'deleteadv_{adv["channel_id"]}'))
            markup.add(InlineKeyboardButton(robot_text['back'], callback_data = 'admin_back_main'))
            bot.edit_message_text('برای حذف کانال مورد نظر بر روی آن کلیک کنید',cid, mid, reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, 'هنوز هیچ کانالی اضافه نشده')


@bot.callback_query_handler(func=lambda call: call.data.startswith("adv"))
def call_callback_panel_sends(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    check = False
    seke = 0 
    number = 0
    for advtest in dict_user_adv[cid]:
        print(cid, advtest)
        if is_user_member(cid, advtest):
            database.insert_advcheck(advtest, cid)
            seke += 400
            number += 1
    if seke!= 0 :
        bot.delete_message(cid, mid)
        info = database.select_user(cid)[0]
        print(info)
        database.update_user(info['inventory']+seke, cid)
        bot.send_message(cid, robot_text['adv_msg'].format(number, seke))

        markup = InlineKeyboardMarkup()
        list_adv = database.select_adv()
        for adv in list_adv:
            check_old_join = database.select_advcheck(adv['channel_id'], cid)
            if is_user_member(cid, adv['channel_id']) == False and len(check_old_join) == 0:
                check = True
                markup.add(InlineKeyboardButton(adv['title'], url = adv['link']))
            markup.add(InlineKeyboardButton('بررسی', callback_data='adv'))

        if check:
            bot.copy_message(cid, channel_text,30, reply_markup=markup)

        # else:
        #     bot.copy_message(cid, channel_text,28)

    else:
        bot.answer_callback_query(call.id, 'شما هنوز داخل هیچ کانالی عضو نشده اید')






@bot.callback_query_handler(func=lambda call: call.data.startswith("sends"))
def call_callback_panel_sends(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data.split("_")  
    count=0  
    count_black=0
    userStep[cid] = 0
    if data[1] =="brodcast":
        list_user=database.select_all_user()
        for i in list_user:
            try:
                bot.copy_message(i['cid'],cid,int(data[-1]))
                count+=1
            except:
                # databases.delete_users(i)
                count_black+=1
                # print("eror")
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("بازگشت",callback_data="admin_back_main"))
        text=f"به {count} نفر ارسال شد"
        if count_black!=0:
            text=f"\n و به {count_black} نفر ارسال نشد احتمالا ربات را بلاک کرده اند و از دیتابیس ما حذف میشوند \n"
        bot.edit_message_text(text,cid,mid,reply_markup=markup)
    if data[1] =="forall":
        list_user=database.select_all_user()
        for i in list_user:
            try:
                bot.forward_message(i['cid'],cid,int(data[-1]))
                count+=1
            except:
                # databases.delete_users(i)
                count_black+=1
                # print("eror")
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("بازگشت",callback_data="admin_back_main"))
        text=f"به {count} نفر ارسال شد"
        if count_black!=0:
            text=f"\n و به {count_black} نفر ارسال نشد احتمالا ربات را بلاک کرده اند و از دیتابیس ما حذف میشوند \n"
        bot.edit_message_text(text,cid,mid,reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data.startswith("hint"))
def def_admin(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data.split("_")
    isinstanc_game = dict_cid_class[cid]
    if int(data[1]) == isinstanc_game.level:
        if isinstanc_game.word_progress != None:
            user_info = database.select_user(cid)[0]
            if user_info['inventory'] >= 90:
                database.update_user(user_info['inventory']-90, cid)
                isinstanc_game.hint()
                check = isinstanc_game.check_completed()
                if check:
                    check_ended = isinstanc_game.insert_completed(isinstanc_game.word_progress)
                    print('check_ended',check_ended)
                    if check_ended == 'ended':
                        database.levelup(cid)
                        dict_cid_class[cid] = utils.game(cid, isinstanc_game.level+1)
                        bot.edit_message_text(get_text_game(cid),cid,mid, reply_markup= show_number_words(cid))
                    else:
                        msg_game(call.message)
                else:
                    msg_game(call.message)

            else:
                bot.answer_callback_query(call.id, 'موجودی سکه شما کمتر از 90 سکه است')
        else:
            bot.answer_callback_query(call.id, 'اول مشخص کنید که چه کلمه ای را کامل میکنید.')
    else:
        bot.edit_message_text('لول شما بالاتر از این مرحله است', cid, mid)

@bot.callback_query_handler(func=lambda call: call.data.startswith("arrived"))
def def_admin(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data.split("_")
    if data[1] == 'accept':
        uid = int(data[2])
        umid = int(data[3])
        seke = int(data[4])
        info_user = database.select_user(cid)[0]
        database.update_user(info_user['inventory']+seke, uid)
        bot.send_message(uid, robot_text['ok_arrived'].format(seke), reply_to_message_id=umid)
        bot.edit_message_reply_markup(cid, mid)
        bot.reply_to(call.message, robot_text['ok_arrived_admin'])

    elif data[1] == 'reject':
        uid = int(data[2])
        umid = int(data[3])
        bot.edit_message_reply_markup(cid, mid)
        bot.send_message(uid, robot_text['no_arrived'], reply_to_message_id=umid)
        bot.reply_to(call.message, robot_text['no_arrived_admin'])


@bot.callback_query_handler(func=lambda call: call.data.startswith("shop"))
def def_admin(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data.split("_")
    if data[1] == 'accept':
        uid = int(data[2])
        umid = int(data[3])
        seke = int(data[4])
        info = database.select_user(uid)[0]
        database.update_user(info['inventory'] + seke , uid)
        bot.edit_message_reply_markup(cid, mid)
        bot.send_message(cid, robot_text['accept_shop'], reply_to_message_id = mid)
        print(data)
        bot.send_message(uid, robot_text['accept_shop_for_uid'].format(seke, info['inventory'] + seke), reply_to_message_id=umid)

    elif data[1] == 'reject':
        uid = int(data[2])
        umid = int(data[3])
        bot.edit_message_reply_markup(cid, mid)
        bot.send_message(cid, robot_text['reject_shop'], reply_to_message_id = mid)
        bot.send_message(uid, robot_text['reject_shop_for_uid'], reply_to_message_id=umid)


    else:
        number_seke = int(data[2])
        stare = int(data[1])
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('قبول کردن', callback_data=f'shop_accept_{cid}_{mid}_{number_seke}'), InlineKeyboardButton('رد کردن', callback_data=f'shop_reject_{cid}_{mid}'))
        print(call.message)
        msg = bot.send_message(admin, robot_text['rezerv_shop'].format('@'+str(call.message.chat.username), f'[{call.message.chat.first_name}](tg://user?id={cid})',number_seke, stare), reply_markup=markup ,parse_mode= 'Markdown')
        bot.reply_to(msg, robot_text['admin_shop_tozih'])
        # bot.delete_message(cid, mid)
        bot.edit_message_reply_markup(cid, mid)
        bot.send_message(cid, robot_text['msg_send_shop'].format(number_seke, stare), reply_markup = reply_markup_main())


@bot.callback_query_handler(func=lambda call: call.data.startswith("buy"))
def def_admin(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data.split("_")
    if data[1] == 'back':
        info_user = database.select_user(cid)[0]
        bot.edit_message_text(robot_text['msg_buy'].format(info_user['inventory']), cid, mid, reply_markup=markup_buy())

    else:
        number_seke = int(data[2])
        price = int(data[1])
        userStep[cid] = 10
        dict_plan_information.setdefault(cid, {})
        dict_plan_information[cid] = {'seke': number_seke, 'price': price}
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(robot_text['cancel'])
        bot.delete_message(cid, mid)
        bot.send_message(cid, robot_text['msg_send_number_cart'].format(number_seke, price), reply_markup = markup)
        # bot.edit_message_text(robot_text['msg_send_number_cart'].format(number_seke, price), cid, mid)
        




@bot.callback_query_handler(func=lambda call: call.data.startswith("letterselect"))
def def_admin(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data.split("_")
    if data[1] == 'selected':
        bot.answer_callback_query(call.id, "حرف انتخاب شده")
    else:
        id_letter = int(data[1])
        isinstanc_game = dict_cid_class[cid]
        if int(data[2]) == isinstanc_game.level:
            if isinstanc_game.word_progress != None:
                check = isinstanc_game.select_letter(id_letter)

                if check == 'no':
                    print(11111111111111111111111)
                    isinstanc_game.wrong_completed()
                    bot.answer_callback_query(call.id, 'اشتباه است')
                    msg_game(call.message)

                elif check:
                    check_ended = isinstanc_game.insert_completed(check)
                    bot.answer_callback_query(call.id, 'عالی بود')
                    if check_ended == 'ended':
                        database.levelup(cid)
                        dict_cid_class[cid] = utils.game(cid, isinstanc_game.level+1)
                        bot.edit_message_text(get_text_game(cid),cid,mid, reply_markup= show_number_words(cid))
                    
                    elif dict_cid_class[cid].letters == 'endgame':
                        database.levelup(cid)
                        dict_cid_class[cid] = utils.game(cid, isinstanc_game.level+1)
                        bot.edit_message_text(get_text_game(cid),cid,mid, reply_markup= show_number_words(cid))   

                    else:
                        msg_game(call.message)

                else:
                    print(3333333333333333)
                    bot.answer_callback_query(call.id, 'انتخاب شد')
                    
                    if dict_cid_class[cid].letters == 'endgame':
                        database.levelup(cid)
                        dict_cid_class[cid] = utils.game(cid, isinstanc_game.level+1)
                        bot.edit_message_text(get_text_game(cid),cid,mid, reply_markup= show_number_words(cid))  
                    else: 
                        msg_game(call.message)
            else:
                bot.answer_callback_query(call.id, 'اول مشخص کنید که چه کلمه ای را کامل میکنید.')
        else:
            bot.edit_message_text('لول شما بالاتر از این مرحله است', cid, mid)
            # bot.edit_message_reply_markup(cid, mid)


@bot.callback_query_handler(func=lambda call: call.data.startswith("wordselect"))
def def_admin(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data.split("_")
    if data[1] == 'completed':
        bot.answer_callback_query(call.id, "کلمه تکمیل شده")
    elif data[1] == 'selected':
        bot.answer_callback_query(call.id, "کلمه انتخابی شما")
    else:
        level = int(data[1])
        word = data[2]
        isinstanc_game = dict_cid_class[cid]
        isinstanc_game.select_word_progress(word)
        msg_game(call.message)

@bot.callback_query_handler(func=lambda call: call.data.startswith("bazyabi"))
def def_admin(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data.split("_")
    isinstanc_game = dict_cid_class[cid]
    if isinstanc_game.word_progress != None:
        isinstanc_game.bazyabi()
        msg_game(call.message)
    else:
        bot.answer_callback_query(call.id, 'اول مشخص کنید که چه کلمه ای را کامل میکنید.')



@bot.callback_query_handler(func=lambda call: call.data.startswith("admin"))
def def_admin(call):
    cid = call.message.chat.id
    if cid == admin :
        mid = call.message.message_id
        data = call.data.split("_")
        if data[1] == 'adv':
            bot.delete_message(cid, mid)
            markup=InlineKeyboardMarkup()
            userStep[cid] = 50 
            markup.add(InlineKeyboardButton("انصراف",callback_data="admin_back_main"))
            bot.copy_message(cid, channel_text,32 , reply_markup=markup) 

        elif data[1] == 'amar':
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="admin_back_main"))
            all_user = database.select_all_user()
            bot.edit_message_text(robot_text['amar'].format(len(all_user)), cid, mid, reply_markup=markup)

        if data[1] == 'cancel':
            bot.delete_message(cid ,mid)
            bot.copy_message(cid, channel_text, 4)
            bot.send_message(cid,robot_text['msg_config'], reply_markup=markup_config_admin())

        if data[1] == 'back':
            if data[2] == 'main':
                userStep[cid] = 0
                bot.edit_message_text(robot_text['msg_config'], cid, mid, reply_markup=markup_config_admin())
            elif data[2] == 'listletters':
                list_dict_letters = database.select_letters()
                markup = InlineKeyboardMarkup()
                for letter in list_dict_letters:
                    markup.add(InlineKeyboardButton(f'لول {letter["level"]}', callback_data=f'admin_editword_{letter["level"]}'))
                markup.add(InlineKeyboardButton(robot_text['back'], callback_data = 'admin_back_main'))
                bot.edit_message_text(robot_text['msg_manage_word'], cid, mid, reply_markup = markup) 

        if data[1] == 'word':

            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(robot_text['cancel'])
            userStep[cid] = 1
            # bot.edit_message_text(robot_text['new_word'].format(get_level()), cid , mid)
            bot.edit_message_reply_markup(cid, mid)
            bot.send_message(cid, robot_text['new_word'].format(get_level()), reply_markup=markup)

        elif data[1] == 'manageword':
            list_dict_letters = database.select_letters()
            markup = InlineKeyboardMarkup()
            for letter in list_dict_letters:
                markup.add(InlineKeyboardButton(f'لول {letter["level"]}', callback_data=f'admin_editword_{letter["level"]}'))
            markup.add(InlineKeyboardButton(robot_text['back'], callback_data = 'admin_back_main'))
            bot.edit_message_text(robot_text['msg_manage_word'], cid, mid, reply_markup = markup)

        elif data[1] == 'editword':
            level = int(data[2])
            dict_letter = database.select_one_letter(level)[0]
            text_words = ''
            for word in database.select_words(level):
                text_words += f'{word["word"]}\n'
            text = robot_text['msg_edit_word'].format(' '.join(dict_letter['letter']), text_words)
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton(robot_text['btn_edit'], callback_data = f'admin_edit_{level}'))
            markup.add(InlineKeyboardButton(robot_text['btn_addword'], callback_data = f'admin_addword_{level}'))
            markup.add(InlineKeyboardButton(robot_text['back'], callback_data = 'admin_back_listletters'))
            bot.edit_message_text(text, cid, mid, reply_markup = markup)

        elif data[1] == 'edit':
            level = int(data[2])
            dict_edit_letters['level'] = level
            bot.delete_message(cid ,mid)
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(robot_text['cancel'])
            userStep[cid] = 3
            bot.send_message(cid, robot_text['edit_word'], reply_markup = markup)

        elif data[1] == 'addword':
            level = int(data[2])
            dict_add_word[cid] = level
            info = database.select_one_letter(level)[0]
            bot.delete_message(cid ,mid)
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(robot_text['cancel'])
            userStep[cid] = 60
            bot.send_message(cid, robot_text['Add_words'].format(level, info['letter']), reply_markup = markup)


        elif data[1]=="brodcast":
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="admin_back_main"))
            bot.edit_message_text("برای ارسال همگانی پیام لطفا پیام خود را ارسال کنید و در غیر این صورت برای بازگشت از دکمه زیر استفاده کنید",cid,mid,reply_markup=markup)
            userStep[cid] = 30
        elif data[1]=="forall":
            markup=InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("بازگشت",callback_data="admin_back_main"))
            bot.edit_message_text("برای فوروارد همگانی پیام لطفا پیام خود را ارسال کنید و در غیر این صورت برای بازگشت از دکمه زیر استفاده کنید",cid,mid,reply_markup=markup)
            userStep[cid] = 31
#-----------------------------------------------------contect_type----------------------------------------
@bot.message_handler(content_types = ['photo'])
def get_photo(m):
    cid=m.chat.id
    mid=m.message_id
    print(m)
    if get_user_step(cid) == 10:
        userStep[cid] == 0
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('قبول کردن', callback_data=f'arrived_accept_{cid}_{mid}_{dict_plan_information[cid]["seke"]}'), InlineKeyboardButton('رد کردن', callback_data=f'arrived_reject_{cid}_{mid}'))
        bot.copy_message(admin, cid, mid, caption=robot_text['capcion_photo'].format('@'+str(m.from_user.username), f'[{m.from_user.first_name}](tg://user?id={cid})',dict_plan_information[cid]['seke'], dict_plan_information[cid]['price']), reply_markup = markup, parse_mode= 'Markdown')
        bot.send_message(cid, robot_text['send_arrive'], reply_markup=reply_markup_main(), reply_to_message_id=mid)
        
    else:
        bot.copy_message(cid, channel_text, 16, reply_markup=reply_markup_main())


#----------------------------------------------------------m.text------------------------------------------------
# ➡ ⬅ 1⃣ 2⃣ 3⃣ 4⃣ 5⃣ 6⃣ 7⃣ 8⃣ 8⃣ 9⃣ 🔟

@bot.message_handler(func=lambda m: m.text.startswith(robot_text['best']))
def handel_text(m):
    cid=m.chat.id
    mid=m.message_id
    list_users = database.select_user_by_leve()
    text = 'نفرات برتر 📊\n'
    number = ['1⃣','2⃣','3⃣','4⃣','5⃣','6⃣','7⃣','8⃣','9⃣','🔟']
    for index in range(len(list_users)):
        text += f'{number[index]}. [{list_users[index]["name"]}](tg://user?id={list_users[index]["cid"]})     ➡     {list_users[index]["level"]} ⚜\n'
    bot.send_message(cid, text, parse_mode='Markdown')




@bot.message_handler(func=lambda m: m.text.startswith(robot_text['buy']))
def handel_text(m):
    cid=m.chat.id
    mid=m.message_id
    info_user = database.select_user(cid)[0]
    bot.send_message(cid, robot_text['msg_buy'].format(info_user['inventory']), reply_markup=markup_buy())
    

@bot.message_handler(func=lambda m: m.text.startswith(robot_text['game']))
def handel_text(m):
    cid=m.chat.id
    mid=m.message_id
    info_user = database.select_user(cid)[0]
    words = database.select_words(info_user['level'])
    dict_cid_class.setdefault(cid,'')
    dict_cid_class[cid] = utils.game(cid, info_user['level'])
    if dict_cid_class[cid].letters == 'endgame':
        if dict_cid_class[cid].level == 0:
            bot.send_message(cid, 'هنوز بازی توسط ادمین اضافه نشده')
        else:
            bot.copy_message(cid, channel_text, 20)
    else:
        bot.send_message(cid, get_text_game(cid), reply_markup= show_number_words(cid))



@bot.message_handler(func=lambda m: m.text.startswith(robot_text['cancel']))
def handel_text(m):
    cid=m.chat.id
    text=m.text
    mid=m.message_id
    if get_user_step(cid) == 10:
        userStep[cid] = 0
        bot.send_message(cid, robot_text['msg_csmcel'], reply_markup=reply_markup_main())
    elif cid == admin:
        dict_edit_letters.clear()
        if cid in dict_new_letters:
            dict_new_letters.pop(cid)
        userStep[cid] = 0
        bot.copy_message(cid, channel_text, 4)
        bot.copy_message(cid, channel_text, 2, reply_markup=markup_config_admin())

@bot.message_handler(func=lambda m: m.text.startswith(robot_text['lagv']))
def handel_text(m):
    cid=m.chat.id
    text=m.text
    mid=m.message_id
    bot.copy_message(cid, channel_text, 16, reply_markup=reply_markup_main())


@bot.message_handler(func=lambda m: m.text in [robot_text['completion'], robot_text['completion_old']])
def handel_text(m):
    cid=m.chat.id
    text=m.text
    mid=m.message_id
    if cid == admin:
        if get_user_step(cid) == 2:
            userStep[cid] = 0
            level = get_level()
            id = database.insert_letters(dict_new_letters[cid], level)
            for word in dict_word[dict_new_letters[cid]]:
                database.insert_word(int(level), word)
            reply_markup = ReplyKeyboardRemove()
            bot.send_message(cid, robot_text['msg_completioned'].format(level), reply_markup = reply_markup)
            bot.copy_message(cid, channel_text, 2, reply_markup=markup_config_admin())

        elif get_user_step(cid) == 4:
            userStep[cid] = 0
            level = dict_edit_letters['level']
            database.update_letters(dict_edit_letters['letters'], level)
            dict_letter = database.select_one_letter(level)[0]
            database.delete_words(int(level))
            for word in dict_edit_letters['words']:
                database.insert_word(int(level), word)
            reply_markup = ReplyKeyboardRemove()
            bot.send_message(cid, robot_text['msg_edited'].format(level), reply_markup = reply_markup)
            bot.copy_message(cid, channel_text, 2, reply_markup=markup_config_admin())


@bot.message_handler(func=lambda m: m.text == robot_text['invite'])
def handel_text(m):
    cid=m.chat.id
    text=m.text
    mid=m.message_id
    info = bot.get_me()
    link = f'https://t.me/{info.username}?start={cid}'
    bot.send_message(cid, robot_text['msg_invite'].format(link))

@bot.message_handler(func=lambda m: m.text == robot_text['shop'])
def handel_text(m):
    cid=m.chat.id
    text=m.text
    mid=m.message_id
    bot.copy_message(cid, channel_text, 24, reply_markup=shop_markup())

@bot.message_handler(func=lambda m: m.text == robot_text['tabligh'])
def handel_text(m):
    cid=m.chat.id
    text=m.text
    mid=m.message_id
    list_adv = database.select_adv()
    if len(list_adv) > 0:
        markup = InlineKeyboardMarkup()
        check = False
        dict_user_adv.setdefault(cid, [])
        dict_user_adv[cid] = []
        # list_adv = database.select_adv()
        for adv in list_adv:
            check_old_join = database.select_advcheck(adv['channel_id'], cid)
            if is_user_member(cid, adv['channel_id']) == False and len(check_old_join) == 0:
                markup.add(InlineKeyboardButton(adv['title'], url=adv['link']))
                dict_user_adv[cid].append(adv['channel_id'])
                check = True
        markup.add(InlineKeyboardButton('بررسی', callback_data='adv'))
        if check:
            bot.copy_message(cid, channel_text, 30, reply_markup= markup)
        else:
            bot.copy_message(cid, channel_text, 28)
        # bot.copy_message(cid, channel_text, 26)
    else:
        bot.copy_message(cid, channel_text, 42)




#---------------------------------------------------------userstep---------------------------------------------------
@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==1)
def defini_word(m):
    cid=m.chat.id
    if cid == admin:
        text=m.text.replace(' ', '')
        dict_new_letters.setdefault(cid,'')
        dict_new_letters[cid] = text
        userStep[cid] = 2
        bot.copy_message(cid, channel_text, 6)


@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==2)
def add_word(m):
    cid=m.chat.id
    if cid == admin:
        word = m.text
        if dict_new_letters[cid] in dict_word:
            if word in dict_word[dict_new_letters[cid]]:
                bot.copy_message(cid, channel_text, 14)
                return
        check = can_form_word(word, dict_new_letters[cid])
        if check:
            dict_word.setdefault(dict_new_letters[cid], [])
            dict_word[dict_new_letters[cid]].append(word)
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(robot_text['completion'])
            markup.add(robot_text['cancel'])
            bot.copy_message(cid, channel_text, 8, reply_markup=markup)
        else:
            if dict_new_letters[cid] in dict_word:
                if len(dict_word[dict_new_letters[cid]]) > 0:
                    markup = ReplyKeyboardMarkup(resize_keyboard=True)
                    markup.add(robot_text['completion_old'])
                    markup.add(robot_text['cancel'])
                else:
                    markup = ReplyKeyboardMarkup(resize_keyboard=True)
                    markup.add(robot_text['cancel'])
            else:
                markup = ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add(robot_text['cancel'])

            bot.copy_message(cid, channel_text, 10, reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==3)
def defini_word(m):
    cid=m.chat.id
    if cid == admin:
        text=m.text.replace(' ', '')
        dict_edit_letters.setdefault('letters','')
        dict_edit_letters['letters'] = text
        userStep[cid] = 4
        bot.copy_message(cid, channel_text, 6)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==4)
def add_word(m):
    cid=m.chat.id
    if cid == admin:
        word = m.text
        check = can_form_word(word, dict_edit_letters['letters'])
        if check:
            dict_edit_letters.setdefault('words', [])
            dict_edit_letters['words'].append(word)
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(robot_text['completion'])
            markup.add(robot_text['cancel'])
            bot.copy_message(cid, channel_text, 8, reply_markup=markup)
        else:
            if len(dict_edit_letters['words']) > 0:
                markup = ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add(robot_text['completion_old'])
                markup.add(robot_text['cancel'])
            else:
                markup = ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add(robot_text['cancel'])

            bot.copy_message(cid, channel_text, 10, reply_markup=markup)


@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==30)
def add_word(m):
    cid=m.chat.id
    mid = m.message_id
    if cid == admin:
        userStep[cid] = 0
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("تایید",callback_data=f"sends_brodcast_{mid}"))
        markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="admin_back_main"))
        bot.send_message(cid,"پیام شما دریافت شد برای ارسال همگانی تایید را بزنید",reply_markup=markup)
    
@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==31)
def add_word(m):
    cid=m.chat.id
    mid = m.message_id
    if cid == admin:
        userStep[cid] = 0
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("تایید",callback_data=f"sends_forall_{mid}"))
        markup.add(InlineKeyboardButton("بازگشت به پنل",callback_data="admin_back_main"))
        bot.send_message(cid,"پیام شما دریافت شد برای فوروارد همگانی تایید را بزنید",reply_markup=markup)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==50)
def add_word(m):
    global rezerv_adv
    cid=m.chat.id
    mid = m.message_id
    if cid == admin:
        print(m)
        if m.forward_from_chat:
            channel_id = m.forward_from_chat.id
            chat_member = bot.get_chat_member(channel_id, bot.get_me().id)
            if chat_member.status in ['administrator', 'creator']:
                check_database = database.select_one_adv(channel_id)
                if len(check_database) == 0:
                    rezerv_adv = [channel_id, m.forward_from_chat.title]
                    userStep[cid] = 51
                    bot.copy_message(cid, channel_text, 38)
                else:
                     bot.send_message(cid, 'این کانال قبلا اضافه شده')
            else:
                bot.copy_message(cid, channel_text, 36)
        else:
            bot.copy_message(cid, channel_text, 34)

@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==51)
def add_word(m):
    global rezerv_adv
    cid=m.chat.id
    mid = m.message_id
    text = m.text
    if cid == admin:
        database.insert_adv(rezerv_adv[0],rezerv_adv[1], text)
        userStep[cid] = 0
        bot.copy_message(cid, channel_text, 40, reply_markup=reply_markup_main())


@bot.message_handler(func=lambda m: get_user_step(m.chat.id)==60)
def add_word(m):
    cid=m.chat.id
    mid = m.message_id
    text = m.text
    if cid == admin:
        level = dict_add_word[cid]
        info_letter = database.select_one_letter(level)[0]
        if can_form_word(text, info_letter['letter']):
            database.insert_word(level, text)
            bot.copy_message(cid, channel_text, 44)
        else:
            bot.copy_message(cid, channel_text, 10)


@bot.message_handler(func=lambda m: True)
def all_msg(m):
    cid=m.chat.id
    if get_user_step(cid) == 10:
        bot.copy_message(cid, channel_text, 18)
    
    else:
        bot.copy_message(cid, channel_text, 16, reply_markup=reply_markup_main())


bot.infinity_polling()