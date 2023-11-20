from telegram import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Update, WebAppInfo, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler, CallbackContext
import json
from adding import check_link
from bs4 import BeautifulSoup
from db import *
prov = '981556791'

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    key = [[KeyboardButton(text="Канал", web_app=WebAppInfo(url="https://pinkgoose136.github.io/pinkgoose.github.io/saitik2.html?type=channels")),
           KeyboardButton(text="Группа", web_app=WebAppInfo(url="https://pinkgoose136.github.io/pinkgoose.github.io/saitik2.html?type=groups")),
           KeyboardButton(text="Бот", web_app=WebAppInfo(url="https://pinkgoose136.github.io/pinkgoose.github.io/saitik2.html?type=bots"))],
           [KeyboardButton(text="Стикерпак", web_app=WebAppInfo(url="https://pinkgoose136.github.io/pinkgoose.github.io/saitik2.html?type=stickers")),
           KeyboardButton(text="Эмодзипак", web_app=WebAppInfo(url="https://pinkgoose136.github.io/pinkgoose.github.io/saitik2.html?type=emoji"))]
            ]
    
    await update.message.reply_text(
        "Выберите тип элемента, который хотите добавить",
        reply_markup=ReplyKeyboardMarkup(key, resize_keyboard=True),
    )

async def aie(update: Update, context: CallbackContext):
    res = json.loads(update.message.web_app_data.data)
    if res['name'] == 'draft':
        try:
            re = await check_link(context, res['type'], res['link'])
            if re['error'] != '':
                await update.message.reply_text(re['error'])
                add_data(res['date'])
            else:
                tex = f"Ссылка: {res['link']}\nОписание: {res['desc']}\nТип: {res['type']}\nКатегория: {get_el(res['cat'])}\nТеги: {get_el(res['tag'])}"
                await update.message.reply_text(tex, reply_markup=ReplyKeyboardRemove())
                btns = [
                [InlineKeyboardButton("Одобрить заявку", callback_data=f"ODOBRIT True {re['link']} {update.message.chat_id}")],
                [InlineKeyboardButton("Удалить", callback_data=f"ODOBRIT False {re['link']} {update.message.chat_id}")],
                [InlineKeyboardButton(text="Check", web_app=WebAppInfo(url="https://pinkgoose136.github.io/pinkgoose.github.io/item.html?idi="+res['date']))]
            ]
                reply_markup = InlineKeyboardMarkup(btns)
                await context.bot.send_message(chat_id=prov, text=tex, reply_markup=reply_markup)
        except Exception as e:
            if 'error' in res.keys():
                await update.message.reply_text(res['error'], reply_markup=ReplyKeyboardRemove())
                add_data(res['date'])
            else:
                await update.message.reply_text(str(e), reply_markup=ReplyKeyboardRemove())
                add_data(res['date'])
    elif res['name'] == 'check':
        await update.message.reply_text(str(res['links']), reply_markup=ReplyKeyboardRemove())

async def question(update, context):
    query = update.callback_query.data
    q = query.split(' ')
    if q[0] == 'ODOBRIT':
        if q[1] == 'False':
            #au = update.callback_query.from_user.id
            #autr = showitem2(connectdb(), 'list', 'name', qu[2], 'author')[0][0]
            #delt(connectdb(), query.split(' ')[2])
            #delclt(connectdb(), query.split(' ')[2])

            await context.bot.send_message(q[3], f'Ваша заявка на добавление https://t.me/{q[2]} не была одобрена', disable_web_page_preview=True)
            chat_id = update.callback_query.message.chat_id
            message_id = update.callback_query.message.message_id
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)

        elif q[1] == 'True':
            omg = []
            bu = update.callback_query.message.text.split('\n')
            for b in bu:
                omg.append(b.split(': ')[1])
            print(omg)
            x1 = [[x, 'category'] for x in omg[3].split(',')]
            x2 = [[x, 'tags'] for x in omg[4].split(',')]
            print(x1+x2)
            add_data(omg[0], omg[1], omg[2], q[3], x1+x2)

            await context.bot.send_message(q[3], f'Ваша заявка на добавление https://t.me/{q[2]} была одобрена', disable_web_page_preview=True)
            await context.bot.send_message(q[3], str(get_data(q[3])), disable_web_page_preview=True)
            chat_id = update.callback_query.message.chat_id
            message_id = update.callback_query.message.message_id
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)

def get_el(el):
    soup = BeautifulSoup(el, 'html.parser')
    if soup != "":
        div_texts = [div.get_text(strip=True) for div in soup.find_all('div')]
        return ", ".join(div_texts)
    else:
        return "Отсутствуют"


async def list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Нажмите на кнопку ниже",
    reply_markup=InlineKeyboardMarkup.from_button(InlineKeyboardButton(text="Открыть каталог",
    web_app=WebAppInfo(url="https://pinkgoose136.github.io/pinkgoose.github.io/list.html"))))


async def alist(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.message.chat_id) == prov: 
        key = [[KeyboardButton(text="Нажмите на кнопку в меню", web_app=WebAppInfo(url="https://pinkgoose136.github.io/pinkgoose.github.io/alist.html"))],]
        
        await update.message.reply_text(
            "Открыть список заявок",
            reply_markup=ReplyKeyboardMarkup(key, resize_keyboard=True),
        )
    else:
        await update.message.reply_text("Данная команда доступна лишь для администрации бота")

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if str(update.message.chat_id) == prov: 
        ke = get_bad_records()
        ap = ""

        for k in ke[1]:
            ap += k[0] + '.'
        ap = ap[:-1]

        await update.message.reply_text("Нажмите на кнопку ниже",
        reply_markup=InlineKeyboardMarkup.from_button(InlineKeyboardButton(text="Очистить неверные заявки",
        web_app=WebAppInfo(url="https://pinkgoose136.github.io/pinkgoose.github.io/bad.html?ids="+ap))))
    else:
        await update.message.reply_text("Данная команда доступна лишь для администрации бота")

def main() -> None:
    application = Application.builder().token("5796993170:AAF51DeZbBIgVTRcmWltWfKM7-JoRa5tAAc").build()
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("list", list))
    application.add_handler(CommandHandler("alist", alist))
    application.add_handler(CommandHandler("clear", clear))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, aie))
    application.add_handler(CallbackQueryHandler(question))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()