import json
import logging
import os
import requests
from bs4 import BeautifulSoup as BeautifulSoup
from telegram import Update

logger = logging.getLogger(__name__)
session_data = {}


def read_grades() -> str:
    global session_data

    html = read_page('https://school.nso.ru/journal-student-grades-action/'+session_data['pupil_id'])
    dom = BeautifulSoup(html, 'html.parser')

    grades = dict()

    for domElement in dom.select('div[mark_date]'):
        if domElement.get('mark_date') != "":
            if domElement.get('name') in grades:
                grades[domElement.get('name')][domElement.get('mark_date')] = domElement.get_text('', True)
            else:
                grades[domElement.get('name')] = dict()

    result_string = ''
    for subject, marks in grades.items():
        result_string += subject
        result_string += ': '
        for date, mark in marks.items():
            result_string += mark + ' '
        result_string += '\n'
    return result_string


def read_homework(shortDate, week: int) -> str:
    global session_data

    html = read_page('https://school.nso.ru/journal-app/'+session_data['pupil_id']+'/week.'+str(week))
    dom = BeautifulSoup(html, 'html.parser')
    result = ''
    for domElement in dom.select('.dnevnik .dnevnik-day'):
        logger.info(domElement.select_one('.dnevnik-day__header .dnevnik-day__title').get_text('', True))
        _, dnevnik_date = domElement.select_one('.dnevnik-day__header .dnevnik-day__title').get_text('', True).split(', ')
        logger.info("%s == %s", dnevnik_date, shortDate)
        if shortDate == dnevnik_date:
            """parse all home task of this day"""
            result += dnevnik_date + " :\n"
            for lessonElement in domElement.select('.dnevnik-day__lessons .dnevnik-lesson'):
                result += lessonElement.select_one('.dnevnik-lesson__subject span').get_text('', True) + '  - '
                home_task_element = lessonElement.select_one('.dnevnik-lesson__hometask .dnevnik-lesson__task')
                if home_task_element:
                    result += '  ' + home_task_element.get_text('', True)
                result += '\n'
            result += '\n'

            return result

    return "Не нашлась домашка за "+shortDate


def save_session_data():
    with open('data/' + os.environ['chat_id'] + '.json', 'w') as outfile:
        outfile.write(json.dumps(session_data))
    pass


def auth(login: str, password: str) -> bool:

    data = {'username': login, 'password': password}

    logger.info(data)

    client = requests.Session()

    response = client.post('https://school.nso.ru/ajaxauthorize', data)
    # todo verify for errors

    logger.info("Auth success \nsession id = %s \n response from auth\n%s \n ", client.cookies['session_id'],
                response.text)

    chat_id = os.environ['chat_id']

    # save session id to file
    global session_data
    session_data = {'chat_id': chat_id, 'session_id': client.cookies['session_id']}

    save_session_data()

    return True


def read_first_page() -> bool:
    html = read_page('https://school.nso.ru/')

    dom = BeautifulSoup(html, 'html.parser')
    link_to_grades = dom.select_one('a[href*="journal-student-grades-action"]')
    s1, s2, pupil_id = link_to_grades.get('href').split('/')
    logger.info("Pupil id\n%s\n ", pupil_id)

    if pupil_id:
        session_data['pupil_id'] = pupil_id
        return True

    return False


def read_page(url: str) -> str:
    cookies = {'school_domain': 'nso1613660760', 'schdomain': 'nso1613660760', 'session_id': session_data['session_id']}

    client = requests.Session()
    response = client.get(url, cookies=cookies)
    logger.info("Read url %s and get status code=%d", url, response.status_code)
    if response.status_code == 200:
        return response.text
    return ''


def is_auth_ok(update: Update) -> bool:
    global session_data
    chat_id = str(get_chat_id(update))
    session_file_name = 'data/' + chat_id + '.json'
    logger.info('session file name ' + session_file_name)
    if os.path.exists(session_file_name):
        with open(session_file_name) as json_file:
            session_data = json.load(json_file)
            logger.info("Session id %s ", session_data['session_id'])
            """ Verify that session id is actual """
            return read_first_page()

    return False


def get_chat_id(update: Update):
    chat_id = None
    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.channel_post is not None:
        chat_id = update.channel_post.chat.id
    return str(chat_id)
