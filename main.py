from pyrogram import Client, filters, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from importlib import reload
from datetime import datetime
import json
import handeler
import os

reload(handeler)

# ---------------------- Configs ---------------------- #
api_id = int(os.getenv("API_ID", 123456))
api_hash = os.getenv("API_HASH", "your_api_hash")
token = os.getenv("BOT_TOKEN", "your_bot_token")

bot = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=token)

# ---------------------- Globals ---------------------- #
data = handeler.readfile()
store = []
logs = 0
actions = {
    'adder': False, 'remover': False, 'finder': False, 'changer': False,
    'saver': False, 'deleter': False, 'sorter': False
}
sc_dataset = ['name', 'lastname', 'job', 'company']

# ---------------------- Helper Functions ---------------------- #
def store_user(pm, user, timer):
    pm.reply_text(
        f'Welcome {pm.chat.first_name} 👋\nDate: {timer[0]} 🗓️\nTime: {timer[1]} 🕐'
    )
    store.append(user)

def show(pm, db):
    if not db:
        pm.reply_text('❌ No data')
        return
    msg = ""
    for idx, val in enumerate(db.values(), 1):
        status = "💾" if val[4] else "⛔"
        msg += (f"#️⃣ <strong>{idx}</strong>\n"
                f"Name: {val[0]}\nLastname: {val[1]}\n"
                f"Job: {val[2]}\nCompany: {val[3]}\nStatus: {status}\n\n")
    pm.reply_text(msg)

def show_people(pm, db):
    if not db:
        pm.reply_text("👥 <strong>0</strong>")
        return
    msg = ""
    for idx, val in enumerate(db.values(), 1):
        msg += f"#️⃣ <strong>{idx}</strong>\n{val[0]}  {val[1]}\n"
    msg += f"\n👥 <strong>{len(db)}</strong>"
    pm.reply_text(msg)

def add_people(pm, db):
    idx = str(len(db))
    entry = pm.text.split()
    entry.append(False)
    db[idx] = entry

def remove_people(pm, db):
    idx = int(pm.text) - 1
    if str(idx) in db:
        db = {str(i): db[str(i)] for i in range(len(db)) if str(i) != str(idx)}
        db = {str(i): val for i, val in enumerate(db.values())}
        save_data(db)

def change_people(pm, db):
    keys = {'name': 0, 'lastname': 1, 'job': 2, 'company': 3}
    parts = pm.text.split()
    idx = int(parts[0]) - 1
    if str(idx) in db and parts[1] in keys:
        db[str(idx)][keys[parts[1]]] = parts[2]

def save_data(db):
    for v in db.values():
        v[4] = True
    with open('data.txt', 'w') as f:
        json.dump(db, f)
    reload(handeler)
    global data
    data = handeler.readfile()

def delete_file():
    with open('data.txt', 'w') as f:
        json.dump({}, f)
    reload(handeler)
    global data
    data = handeler.readfile()

def sort_file(pm, db):
    keys = {'name': 0, 'lastname': 1, 'job': 2, 'company': 3}
    sorted_items = sorted(db.items(), key=lambda x: x[1][keys[pm.text.lower()]])
    db_sorted = {str(i): item[1] for i, item in enumerate(sorted_items)}
    for v in db_sorted.values():
        v[4] = False
    with open('data.txt', 'w') as f:
        json.dump(db_sorted, f)
    reload(handeler)
    global data
    data = handeler.readfile()

# ---------------------- Help Message ---------------------- #
helper_message = '''You can control me with these commands:
/cmd — Show menu
/help — Show help
/time — Get current time
/cancel — Cancel current action

🔁 Actions:
- Add: name lastname job company
- Remove: index
- Change: index field new_value
- Find: lastname
- Sort: name|lastname|job|company
- Save: confirm
- Delete all: confirm

📦 Status:
💾 Saved
⛔ Not saved
❌ Empty
'''

# ---------------------- Handlers ---------------------- #
@bot.on_message(filters.text & filters.private)
def main_handler(c, m):
    global logs, actions
    username = m.chat.username
    time_now = datetime.utcfromtimestamp(m.date + 16200).strftime('%Y-%m-%d %H:%M:%S').split()
    logs += 1
    print(f'{logs} {username} {time_now}')

    keyboard = ReplyKeyboardMarkup(
        [['1', '2', '3'], ['Cmd', 'Help', 'Time'], ['Name', 'Lastname', 'Job', 'Company']],
        resize_keyboard=True
    )
    c.send_message(username, "Loading ⏳", reply_markup=keyboard)

    txt = m.text.lower()

    if username not in store:
        store_user(m, username, time_now)
        c.send_message(username, "**Use /cmd or /help to begin.**")

    elif txt in {'help', '/help'}:
        c.send_message(username, f"**{helper_message}**")

    elif txt in {'time', '/time'}:
        c.send_message(username, f"Date: {time_now[0]} 🗓️\nTime: {time_now[1]} 🕐")

    elif txt in {'cmd', '/cmd'}:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('📃Show', callback_data='show'),
             InlineKeyboardButton('👥People', callback_data='show_people')],
            [InlineKeyboardButton('✅Add', callback_data='add'),
             InlineKeyboardButton('❌Remove', callback_data='remove')],
            [InlineKeyboardButton('🔍Find', callback_data='find'),
             InlineKeyboardButton('📄Change', callback_data='change')],
            [InlineKeyboardButton('💾Save', callback_data='save'),
             InlineKeyboardButton('🗑️Delete all', callback_data='delete')],
            [InlineKeyboardButton('🔢Sort', callback_data='sort')]
        ])
        c.send_message(username, "----Commands----", reply_markup=keyboard)

    elif actions['adder']:
        parts = m.text.split()
        if txt in {'cancel', '/cancel'}:
            actions['adder'] = False
            c.send_message(username, "❌ Canceled")
        elif len(parts) == 4 and all(not x.isdigit() for x in parts):
            add_people(m, data)
            actions['adder'] = False
            c.send_message(username, "✅ Added")
        else:
            c.send_message(username, "⚠️ Invalid input")

    elif actions['remover']:
        if txt in {'cancel', '/cancel'}:
            actions['remover'] = False
            c.send_message(username, "❌ Canceled")
        elif txt.isdigit() and int(txt) <= len(data):
            remove_people(m, data)
            actions['remover'] = False
            c.send_message(username, "✅ Removed")
        else:
            c.send_message(username, "⚠️ Invalid index")

    elif actions['finder']:
        if txt in {'cancel', '/cancel'}:
            actions['finder'] = False
            c.send_message(username, "❌ Canceled")
        else:
            found = next((v for v in data.values() if v[1] == m.text), None)
            if found:
                status = "💾" if found[4] else "⛔"
                msg = (f"Name: {found[0]}\nLastname: {found[1]}\n"
                       f"Job: {found[2]}\nCompany: {found[3]}\nStatus: {status}")
                actions['finder'] = False
                c.send_message(username, msg)
            else:
                c.send_message(username, "⚠️ Not found")

    elif actions['changer']:
        if txt in {'cancel', '/cancel'}:
            actions['changer'] = False
            c.send_message(username, "❌ Canceled")
        elif len(m.text.split()) == 3:
            change_people(m, data)
            actions['changer'] = False
            c.send_message(username, "✅ Changed")
        else:
            c.send_message(username, "⚠️ Invalid input")

    elif actions['saver']:
        if txt == 'confirm':
            save_data(data)
            actions['saver'] = False
            c.send_message(username, "✅ Saved")
        elif txt in {'cancel', '/cancel'}:
            actions['saver'] = False
            c.send_message(username, "❌ Canceled")
        else:
            c.send_message(username, "⚠️ Invalid input")

    elif actions['deleter']:
        if txt == 'confirm':
            delete_file()
            actions['deleter'] = False
            c.send_message(username, "✅ Deleted")
        elif txt in {'cancel', '/cancel'}:
            actions['deleter'] = False
            c.send_message(username, "❌ Canceled")
        else:
            c.send_message(username, "⚠️ Invalid input")

    elif actions['sorter']:
        if txt in sc_dataset:
            sort_file(m, data)
            actions['sorter'] = False
            c.send_message(username, f"✅ Sorted by {txt}")
        elif txt in {'cancel', '/cancel'}:
            actions['sorter'] = False
            c.send_message(username, "❌ Canceled")
        else:
            c.send_message(username, "⚠️ Invalid sort key")

    elif txt in {'cancel', '/cancel'}:
        c.send_message(username, "⚠️ No active action to cancel")

    else:
        c.send_message(username, f'⚠️ "{m.text}" not recognized. Try /cmd or /help.')

# ---------------------- Callback Queries ---------------------- #
@bot.on_callback_query()
def callback_handler(c, query):
    global actions
    query.answer("Action selected")

    if list(actions.values()).count(True):
        c.send_message(query.from_user.username, "⚠️ Action already in progress")
        return

    cb = query.data
    if cb == 'show':
        show(query.message, data)
    elif cb == 'show_people':
        show_people(query.message, data)
    elif cb in actions:
        actions[cb] = True
        prompts = {
            'add': "Enter: Name Lastname Job Company",
            'remove': "Enter index to remove",
            'find': "Enter lastname to find",
            'change': "Enter: Index Field NewValue",
            'save': "Type confirm to save",
            'delete': "Type confirm to delete all",
            'sort': "Enter field to sort by: name|lastname|job|company"
        }
        c.send_message(query.from_user.username, prompts[cb])

# ---------------------- Start Bot ---------------------- #
bot.run()
# --------------------------------#
#       #Phonebookbot             #
# - Author    : Emad Ramezani     #
# - Date      : 08/08/2021        #
# --------------------------------#
# - Refactored 
# - Date      : 06/04/2025


