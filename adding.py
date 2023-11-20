from bs4 import BeautifulSoup
import requests
from dotdb import *
from bubris import cats, bot_channels, sho
from telegram.constants import ParseMode

async def check_link(updater, type, lnk):
    error = False
    err = ''
    changetyp = ''
    if type in ['groups', 'channels']:
        er1 = ''
        if type == 'groups':
            er1 = 'Группа не найдена'
        elif type == 'channels':
            er1 = 'Калал не найден'
        try:
            pa = requests.get(lnk).text
        except:
            error = True
            er1 = "Ссылка указана неверно"
            pa = None

        if pa != None:
            pag = BeautifulSoup(pa, 'html.parser')
            try:
                e = pag.find('div', class_='tgme_page_extra').text.split(',')[0].split()[-1]
                tgnam = pag.find('div', class_='tgme_page_title').text.replace('\n', '')
                img = pag.find('img', class_='tgme_page_photo_image')
                if img != None:
                    img = img.get('src')
                else:
                    img = None
                if e in ['members', 'member'] and type == 'groups':
                    typ = 'group'
                elif e in ['subscriber', 'subscribers'] and type == 'channels':
                    typ = 'channel'
                else:
                    error = True
                    err = er1
            except:
                error = True
                err = er1
        else:
            error = True
            err = er1
    elif type in ['emoji', 'stickers']:
        try:
            sett = await updater.bot.get_sticker_set(lnk.split('/')[-1])
            iu = sett['stickers']
            imgu = iu[0]['file_id']
            imm = await updater.bot.get_file(imgu)
            img = imm['file_path']
            tgnam = sett['title']
            be = BeautifulSoup(requests.get(lnk).text, 'html.parser').find('div', class_='tgme_page_description').text.split()
            typ = be[-2]
            if typ == 'sticker':
                typ += 's'
            changetyp = typ
        except:
            error = True
            err = "Набор не найден"

    elif type == 'bots':
        if lnk.split('/')[-1][-3:].lower() == 'bot':
            pag = BeautifulSoup(requests.get(lnk).text, 'html.parser')
            t = pag.find('div', class_='tgme_page_title')
            if t == None:
                error = True
                err = "Бот не найден"
            else:
                tgnam = pag.find('div', class_='tgme_page_title').text.replace('\n', '')
                imgg = pag.find('img', class_='tgme_page_photo_image')
                if imgg != None:
                    img = imgg.get('src')
                else:
                    img = None
        else:
            error = True
            err = "Бот не найден"
    if error == True:
        return {'error': err}
    else:
        return {'img': img, 'tgnam': tgnam, 'changetyp': changetyp, 'error': '', 'lnk': lnk}

def getimage(linkid):
    lnk = 'https://t.me/' + linkid
    pag = BeautifulSoup(requests.get(lnk).text, 'html.parser')
    imgg = pag.find('img', class_='tgme_page_photo_image')
    if imgg != None:
      img = imgg.get('src')
    else:
      img = None
    return img

def createmes(updater, nam):
    ete = showitem(connectdb(), 'list', 'name', nam)[0]
    et = []
    for ee in ete:
        et.append(ee)
    cltt = showclt(connectdb(), et[0])
    ta = ""
    for c in cltt:
        if c[0] == cltt[-1][0]:
            ta += '#' + cats[et[2]][c[0]]
        else:
            ta += '#' + cats[et[2]][c[0]] + ', '
    if et[2] in ['emoji', 'stickers']:
        linka = 'https://t.me/addstickers/' + et[0]
        sett = updater.bot.get_sticker_set(et[0])
        iu = sett['stickers']
        imgu = iu[0]['thumb']['file_id']
        img = updater.bot.get_file(imgu)['file_path']
    else:
        linka = 'https://t.me/' + et[0]
        img = getimage(et[0])
    tgnam = et[4]

    essa = f"**[{tgnam}]({linka})**\n{et[1]}\n\nКатегории: {ta}\n\n[Добавить {sho[et[2]]} в каталог](https://t.me/Tg_ExplorerBot)"

    if img == None:
        mes = updater.bot.send_photo(chat_id='@'+bot_channels[et[2]], caption=essa, parse_mode=ParseMode.MARKDOWN, photo=open('empty.png', 'rb'))
    else:
        response = requests.get(img).content
        mes = updater.bot.send_photo(chat_id='@'+bot_channels[et[2]], caption=essa, parse_mode=ParseMode.MARKDOWN, photo=response)
    edit_item(connectdb(), 'idpost', mes.message_id, et[0])
    return [linka, '@'+bot_channels[et[2]]]