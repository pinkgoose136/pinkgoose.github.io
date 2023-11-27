from telegram import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Update, WebAppInfo, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler, CallbackContext
import json
from adding import check_link
from bs4 import BeautifulSoup
from db import *
import requests
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
                response = requests.get(re['img'])
                if response.status_code == 200:
                    with open(f"tgex/img/img-{res['date']}.jpg", 'wb') as file:
                        file.write(response.content)
                await update.message.reply_text("Данные успешно получены, осталось подтвердить отправку заявки", reply_markup=ReplyKeyboardRemove())
                await update.message.reply_text("Нажмите на кнопку ниже",
                    reply_markup=InlineKeyboardMarkup.from_button(InlineKeyboardButton(text="Подтвердите отправку заявки",
                    web_app=WebAppInfo(url=f"https://pinkgoose136.github.io/pinkgoose.github.io/item.html?idi={res['date']}&name={re['tgnam']}&img={re['img']}"))))

        except Exception as e:
            if 'error' in res.keys():
                await update.message.reply_text(res['error'], reply_markup=ReplyKeyboardRemove())
                add_data(res['date'])
            else:
                await update.message.reply_text(str(e), reply_markup=ReplyKeyboardRemove())
                add_data(res['date'])
    elif res['name'] == 'check':
        rer = res['links']
        abe = rer.keys()
        for t in abe:
            u = rer[t]
            kt = ''
            if u['answer'] == "NO": 
                kt = ' не '
            await context.bot.send_message( int(u['owner']), f'Ваша заявка на добавление {u["link"] }{kt} была одобрена', disable_web_page_preview=True)

        if rer == '':
            rer = 'Пусто'
        await update.message.reply_text('Готово', reply_markup=ReplyKeyboardRemove())

def get_el(el):
    soup = BeautifulSoup(el, 'html.parser')
    if soup != "":
        div_texts = [div.get_text(strip=True) for div in soup.find_all('div')]
        return ", ".join(div_texts)
    else:
        return "Отсутствуют"

async def kete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Нажмите на кнопку ниже",
    reply_markup=InlineKeyboardMarkup.from_button(InlineKeyboardButton(text="Открыть каталог",
    web_app=WebAppInfo(url="https://pinkgoose136.github.io/pinkgoose.github.io/kete.html"))))

async def bad(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Нажмите на кнопку ниже",
    reply_markup=InlineKeyboardMarkup.from_button(InlineKeyboardButton(text="Открыть каталог",
    web_app=WebAppInfo(url="https://pinkgoose136.github.io/pinkgoose.github.io/bad.html"))))

async def list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Нажмите на кнопку ниже",
    reply_markup=InlineKeyboardMarkup.from_button(InlineKeyboardButton(text="Открыть каталог",
    web_app=WebAppInfo(url="https://pinkgoose136.github.io/pinkgoose.github.io/list.html"))))

async def mylist(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Нажмите на кнопку ниже",
    reply_markup=InlineKeyboardMarkup.from_button(InlineKeyboardButton(text="Открыть каталог",
    web_app=WebAppInfo(url="https://pinkgoose136.github.io/pinkgoose.github.io/my_items.html"))))


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
    application.add_handler(CommandHandler("kete", kete))
    application.add_handler(CommandHandler("bad", bad))
    application.add_handler(CommandHandler("mylist", mylist))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, aie))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
