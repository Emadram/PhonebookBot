from pyrogram import Client, filters, emoji, types
from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                            ReplyKeyboardMarkup, Message)
from importlib import reload
from string import ascii_lowercase
from datetime import datetime
import json
import handeler

reload(handeler)

api_hash = 'api_hash'
api_id = #api_id
token = 'bot_token'
bot = Client(session_name='my_bot', api_id=api_id, api_hash=api_hash, bot_token=token)


# ----------------------------------function part-------------------------------------- #
def store_user(pm, user, timer):  # function for username
    pm.reply_text(f'Welcome {pm.chat.first_name}  \U0001f44b\n'
                  f'Date: {timer[0]} \U0001f5d3\ufe0f\nTime: {timer[1]}      \U0001f570\ufe0f')
    store.append(user)


def show(pm, db):  # show function
    output = ''
    count = 0  # indexer
    if len(db) != 0:
        for i in range(len(db)):
            count += 1
            output += f'#\ufe0f\u20e3 <strong>{count}</strong>\n'
            output += f'Name:  {db[str(i)][0]}\nLastname:  {db[str(i)][1]}\n'
            output += f'Job:  {db[str(i)][2]}\nCompany:  {db[str(i)][3]}\n'
            if db[str(i)][4]:
                output += 'Status:  \U0001f4be\n'
            else:
                output += 'Status:  \u26d4\n'
        pm.reply_text(output)
    else:
        output += '*\ufe0f\u20e3'
        pm.reply_text(output)


def show_people(pm, db):  # people function
    output = ''
    count = 0  # indexer
    if len(db) != 0:
        for i in range(len(db)):
            count += 1
            output += f'#\ufe0f\u20e3 <strong>{count}</strong>\n'
            output += f'{data[str(i)][0]}  {data[str(i)][1]}\n'
        output += f'\n\U0001f465 <strong>{count}</strong>'
        pm.reply_text(output)
    else:
        output += f'\n\U0001f465 <strong>{count}</strong>'
        pm.reply_text(output)


def add_people(pm, db):  # add function
    index = len(db)
    output = pm.text.split()
    output.append(False)  # we have not save it yet
    db[str(index)] = output
    print(db)


def remove_people(pm, db):  # remove function
    index = int(pm.text) - 1
    if len(db) != 0:
        del db[str(index)]
        for i in range(len(db)):  # to fix index of keys
            if str(i) not in db:
                db[str(i)] = db[str(i + 1)]
                del db[str(i + 1)]


def change_people(pm, db):  # change function
    switch_case = {'name': 0,
                   'lastname': 1,
                   'job': 2,
                   'company': 3}
    checker = pm.text.split()
    index = int(checker[0]) - 1
    db[str(index)][switch_case[checker[1]]] = checker[2]


def save_file(db):  # save function
    global data
    for i in range(len(db)):
        db[str(i)][4] = True
    with open('data.txt', 'w') as new_file:
        json.dump(db, new_file)
    reload(handeler)
    data = handeler.readfile()


def delete_file():  # delete function
    global data
    with open('data.txt', 'w') as f:
        json.dump({}, f)
    reload(handeler)
    data = handeler.readfile()


def sort_file(pm, db):  # sort function
    global data
    switch_case = {'name': 0,
                   'lastname': 1,
                   'job': 2,
                   'company': 3}
    db = dict(sorted(db.items(), key=lambda item: item[1][switch_case[pm.text.lower()]]))
    new_db = list(db.values())
    db = {}
    for i in range(len(new_db)):  # fix index for sort
        db[str(i)] = new_db[i]
    for i in range(len(db)):
        db[str(i)][4] = False  # not saved
    with open('data.txt', 'w') as new_file:
        json.dump(db, new_file)
    reload(handeler)
    data = handeler.readfile()


# ----------------------------------variables part-------------------------------------- #
data = handeler.readfile()  # stored data
store = []  # to store usernames
logs = 0  # for logs
actions = {'adder': False, 'remover': False, 'finder': False,'changer': False,'saver': False,
           'deleter': False,'sorter': False} # actions dict
sc_dataset = ['name', 'lastname', 'job', 'company']
# -----------------------------------Help message part---------------------------------- #
helper_message = '''You can control me by sending these commands: 
/cmd => Shows Menu of commands
/help => Shows this text
/cancel => Use it to cancel an action
/time => To see Date and Time
"**You can also use keyboard**" 

"**All of the commands are not case sensitive**"

\U0001f4c4change:
Dataset  => [name,lastname,job,company] for e.g:
1- index => 2
2- What to be changed => job
3- TO what => Developer

\u2705Add:
1- name => reza
2- lastname => mohamadi
3- job => coder
4- company => Roster

\u274cRemove:
1- index => 2

\U0001f50eFind:
1- lastname => razavi

\U0001f4beSave & \U0001f5d1\ufe0fDelete all:
If you are sure just type "**confirm**"

\U0001f521Sort:
Dataset => [name,lastname,job,company]
1- type what you want to sort by => name

\U0001f4c3Show & \U0001f465show_people:
Quick action commands

Status:
\U0001f4beSaved
\u26d4Not saved
*\ufe0f\u20e3Nodata or empty file 
'''


# ----------------------------------Main part------------------------------------------- #


@bot.on_message(filters.text & filters.private)
def app(sender: Client, message):
    global logs, actions  #global part
    username = message.chat.username
    timeuser = datetime.utcfromtimestamp(message.date + 16200).strftime('%Y-%m-%d %H:%M:%S')
    timeuser = timeuser.split()
    logs += 1
    print(f'{logs} {username} {timeuser}')
    bot.send_message(
        f"{username}",  # Edit this
        "Loading\u23f3",
        reply_markup=ReplyKeyboardMarkup(
            [
                ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],  #First row
                ['Cmd', 'Help', 'Time', 'Cancel', 'Confirm'],  #sec row
                ['Name', 'Lastname', 'Job', 'Company']  #third row

            ],
            resize_keyboard=True  # Make the keyboard smaller
        )
    )

    if username not in store:
        store_user(message, username, timeuser)
        msg_new = '**To use commands Type /cmd or /help for help (not case sensitive)** or use Keyboard'
        bot.send_message(chat_id=username, text=f'{msg_new}')

    elif message.text.lower() == 'help' or message.text == '/help':
        bot.send_message(chat_id=username, text=f'**{helper_message}**')

    elif message.text.lower() == 'time' or message.text == '/time':
    	bot.send_message(chat_id=username, text=f'Date: {timeuser[0]} \U0001f5d3\ufe0f\n'
                                                f'Time: {timeuser[1]}      \U0001f570\ufe0f')

    elif message.text.lower() == 'cmd' or message.text == '/cmd':
        # ----------------------------------Inlinekeyboard part------------------------------------------- #
        start_show = types.InlineKeyboardButton(text='\U0001f4c3Show', callback_data='show')
        start_show_people = types.InlineKeyboardButton(text='\U0001f465show_people', callback_data="show_people")
        start_add = types.InlineKeyboardButton(text='\u2705Add', callback_data='add')
        start_remove = types.InlineKeyboardButton(text='\u274cRemove', callback_data='remove')
        start_find = types.InlineKeyboardButton(text='\U0001f50eFind', callback_data='find')
        start_change = types.InlineKeyboardButton(text='\U0001f4c4Change', callback_data='change')
        start_save = types.InlineKeyboardButton(text='\U0001f4beSave', callback_data='save')
        start_delete = types.InlineKeyboardButton(text='\U0001f5d1\ufe0fDelete all', callback_data='delete')
        start_sort = types.InlineKeyboardButton(text='\U0001f521Sort', callback_data='sort')

        start_keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=[[start_show, start_show_people], [start_add, start_remove], [start_find, start_change],
                             [start_save, start_delete], [start_sort]])
        bot.send_message(username, '----Commands----', reply_markup=start_keyboard)

        # ----------------------------------query part---------------------------------------------- #
        @bot.on_callback_query()
        def start_callback(csend: Client, callback_query):
            global actions #global part
            callback_query.answer(f'Button cooldown', show_alert=True)

            # ----------------------------------show part------------------------------------------- #
            if callback_query.data == 'show':
                show(message, data)  # function call

            # ----------------------------------show_people part------------------------------------ #
            elif callback_query.data == 'show_people':
                show_people(message, data)  # function call

            # ----------------------------------Action holder part---------------------------------- #
            elif list(actions.values()).count(True) != 0:
                bot.send_message(chat_id=username, text='**\u26a0\ufe0fA action is available right now**')
            # ----------------------------------add part-------------------------------------------- #
            elif callback_query.data == 'add':
                actions['adder'] = True
                bot.send_message(chat_id=username, text='**Enter details as shown below to add (Shift+Enter)**')
                bot.send_message(chat_id=username,
                                 text='**Name:**\n**Lastname:**\n**Job**:\n**Company:**\n')

            # ----------------------------------remove part------------------------------------------------- #
            elif callback_query.data == 'remove':
                show(message, data)  # function call
                actions['remover'] = True
                bot.send_message(chat_id=username, text='** Enter index of person you want to remove **')

            # ----------------------------------find part------------------------------------------------- #
            elif callback_query.data == 'find':
                actions['finder'] = True
                bot.send_message(chat_id=username, text='** Enter the lastname of person you want to find **')

            # ----------------------------------change part------------------------------------------------- #
            elif callback_query.data == 'change':
                show(message, data)  # function call
                actions['changer'] = True
                bot.send_message(chat_id=username, text='**Enter details as shown below to change (Shift+Enter)**')
                bot.send_message(chat_id=username,
                                 text='**Index:**\n**What to be changed e.g  (job):**\n**To what e.g  (Developer):**')
            # ----------------------------------save part--------------------------------------------------- #
            elif callback_query.data == 'save':
                actions['saver'] = True
                bot.send_message(chat_id=username, text='**Enter confirm to save data**')
            # ----------------------------------delete part--------------------------------------------------- #
            elif callback_query.data == 'delete':
                actions['deleter'] = True
                bot.send_message(chat_id=username, text='**Enter confirm to delete data**')
            # ----------------------------------sort part----------------------------------------------------- #
            elif callback_query.data == 'sort':
                actions['sorter'] = True
                bot.send_message(chat_id=username, text='**Enter how you want to sort by :**')

    # ----------------------------------add conditions part------------------------------------------- #
    elif actions['adder']:  # for adding a user
        check_digit = [ele for ele in message.text.split() if ele.isdigit()]
        if len(check_digit) == 0 and len(message.text.split()) == 4:
            actions['adder'] = False
            add_people(message, data)  # function call
            bot.send_message(chat_id=username, text=f'**\u2705Added successfully**')
        elif message.text.lower() == 'cancel' or message.text == '/cancel':
            actions['adder'] = False
            bot.send_message(chat_id=username, text=f'**Canceled\u26d4**')
       	elif len(check_digit) != 0 and len(message.text.split()) == 4:
       		bot.send_message(chat_id=username, text=f'\u26a0\ufe0fExpected string got int instead **Try again**')
        else:
            bot.send_message(chat_id=username, text=f'\u26a0\ufe0fError not enough values to unpack **Try again**')

    # ----------------------------------remove conditions part------------------------------------------- #
    elif actions['remover']:
        if message.text.isdigit() and int(message.text) <= len(data) != 0:
            actions['remover'] = False
            remove_people(message, data)  # function call
            bot.send_message(chat_id=username, text=f'**\u2705Removed successfully**')
        elif message.text.lower() == 'cancel' or message.text == '/cancel':
            actions['remover'] = False
            bot.send_message(chat_id=username, text=f'**Canceled\u26d4**')
        else:
            bot.send_message(chat_id=username, text=f'\u26a0\ufe0fError index out of range **Try again**')
    # ----------------------------------find conditions part------------------------------------------- #
    elif actions['finder']:
        data_values = []
        for i in range(len(data)):
            data_values.append(data[str(i)][1])
        if message.text in data_values:
            actions['finder'] = False
            idx = data_values.index(message.text)  # indexer
            output = f'**Name: {data[str(idx)][0]}\nLastname: {data[str(idx)][1]}\n**'
            output += f'**Job: {data[str(idx)][2]}\nCompany: {data[str(idx)][3]}\n**'
            if data[str(idx)][4]:
                output += 'Status:  \U0001f4be\n'
            else:
                output += 'Status:  \u26d4\n'
            bot.send_message(chat_id=username, text=output)
        elif message.text.lower() == 'cancel' or message.text == '/cancel':
            actions['finder'] = False
            bot.send_message(chat_id=username, text=f'**Canceled\u26d4**')
        else:
            bot.send_message(chat_id=username, text=f'\u26a0\ufe0fError lastname not found **Try again**')
    # ----------------------------------change conditions part------------------------------------------- #
    elif actions['changer']:
        if message.text.lower() == 'cancel' or message.text == '/cancel':
            actions['changer'] = False
            bot.send_message(chat_id=username, text=f'**Canceled\u26d4**')
        elif len(message.text.split()) == 3 and message.text.split()[1] in sc_dataset:
            actions['changer'] = False
            change_people(message, data)
            bot.send_message(chat_id=username, text=f'**\u2705Changed successfully**')
        else:
            bot.send_message(chat_id=username, text=f'\u26a0\ufe0fError not enough values to unpack **Try again**')
    # ----------------------------------save conditions part------------------------------------------- #
    elif actions['saver']:
        if message.text.lower() == 'confirm':
            actions['saver'] = False
            save_file(data)
            bot.send_message(chat_id=username, text=f'**\u2705Saved successfully**')
        elif message.text.lower() == 'cancel' or message.text == '/cancel':
            actions['saver'] = False
            bot.send_message(chat_id=username, text=f'**Canceled\u26d4**')
        else:
            bot.send_message(chat_id=username, text=f'\u26a0\ufe0fError Invalid **Try again**')
    # ----------------------------------delete conditions part------------------------------------------- #
    elif actions['deleter']:
        if message.text.lower() == 'confirm':
            actions['deleter'] = False
            delete_file()
            bot.send_message(chat_id=username, text=f'**\u2705Deleted successfully**')
        elif message.text.lower() == 'cancel' or message.text == '/cancel':
            actions['deleter'] = False
            bot.send_message(chat_id=username, text=f'**Canceled\u26d4**')
        else:
            bot.send_message(chat_id=username, text=f'\u26a0\ufe0fError Invalid **Try again**')

    # ----------------------------------sort conditions part------------------------------------------- #
    elif actions['sorter']:
        if not message.text.isdigit() and message.text.lower() in sc_dataset:
            actions['sorter'] = False
            sort_file(message, data)
            bot.send_message(chat_id=username, text=f'**\u2705Sorted by {message.text} successfully**')
        elif message.text.lower() == 'cancel' or message.text == '/cancel':
            actions['sorter'] = False
            bot.send_message(chat_id=username, text=f'**Canceled\u26d4**')
        else:
            bot.send_message(chat_id=username, text=f'\u26a0\ufe0fError Invalid **Try again**')

    # ----------------------------------else conditions part------------------------------------------- #
    elif message.text.lower() == 'cancel' or message.text == '/cancel':
        bot.send_message(chat_id=username, text=f'\u26a0\ufe0f No action is available to be canceled')
    else:
        replay_message = 'command not found Try **/cmd** or **/help**'
        bot.send_message(chat_id=username, text=f'\u26a0\ufe0f "{message.text}"  {replay_message} ')

bot.run()

# --------------------------------#
#       #Phonebookbot             #
# - Author    : Emad Ramezani     #
# - Date      : 08/08/2021        #
# --------------------------------#