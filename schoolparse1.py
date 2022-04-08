import requests
from bs4 import BeautifulSoup as bs
import codecs

from datetime import datetime
import pytz

nso_tz = pytz.timezone('Asia/Novosibirsk')
print(nso_tz)


# html_homework = requests.get('https://school.nso.ru/journal-app')

fileObj = codecs.open("homework.html", "r", "utf_8_sig")
html_homework = fileObj.read() # или читайте по строке
fileObj.close()
soup_homework = bs(html_homework, 'html.parser')

current_date = datetime.date(datetime.now(tz=nso_tz))
date_nso = current_date.strftime('%d.%m')
date_nso_a = current_date.strftime('%A')

if date_nso_a == 'Monday':
    date_nso_a = 'Понедельник,'
    date_nso_a += ' ' + date_nso
elif date_nso_a == 'Tuesday':
    date_nso_a = 'Вторник,'
    date_nso_a += ' ' + date_nso
elif date_nso_a == 'Wednesday':
    date_nso_a = 'Среда,'
    date_nso_a += ' ' + date_nso
elif date_nso_a == 'Thursday':
    date_nso_a = 'Четверг,'
    date_nso_a += ' ' + date_nso
elif date_nso_a == 'Friday':
    date_nso_a = 'Пятница,'
    date_nso_a += ' ' + date_nso
elif date_nso_a == 'Saturday':
    date_nso_a = 'Суббота,'
    date_nso_a += ' ' + date_nso
else:
    date_nso == 'Завтра выходной'
print(date_nso_a)

homework = dict()

for el in soup_homework.select('#dnevnikDays'):
    for el in soup_homework.select('.dnevnik-day'):
        if el.get('.dnevnik-day__title') == date_nso_a:
            for el in soup_homework.select('.dnevnik-day__lessons'):
                homework[el.text('.dnevnik-day__lessons')] = dict()
print(homework)