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
            if not (domElement.get('name') in grades):
                grades[domElement.get('name')] = dict()

            # logger.info('grades[%s][%s]=%s', domElement.get('name'), domElement.get('mark_date'), domElement.get_text('', True))
            grades[domElement.get('name')][domElement.get('id')] = domElement.get_text('', True)


    result_string = ''
    for subject, marks in grades.items():
        avg_grades = []
        result_string += subject
        result_string += ': '
        for date, mark in marks.items():
            if mark == 'Н' or mark == 'Б' or mark == '':
                continue
            elif '✕' in mark:
                mark = mark.replace('-', '')
                xnumber = mark.find('✕')
                logger.info(int(mark[xnumber+1]))
                for i in range(int(mark[xnumber+1])):
                    if '/' in mark[:xnumber]:
                        avg_element = int(mark[0])
                        avg_grades.append(avg_element)
                    elif int(mark[:xnumber]) > 10:
                        avg_element = (int(mark[0]) + int(mark[1])) / 2
                        avg_grades.append(avg_element)
                    else:
                        avg_element = int(mark[:xnumber])
                        avg_grades.append(avg_element)
            else:
                mark = mark.replace('-', '')
                if '/' in mark:
                    avg_element = int(mark[0])
                    avg_grades.append(avg_element)
                elif int(mark) > 10:
                    avg_element = (int(mark[0]) + int(mark[1])) / 2
                    avg_grades.append(avg_element)
                else:
                    avg_element = int(mark)
                    avg_grades.append(avg_element)
            grades_sum = 0
            logger.info(avg_grades)
            for element in avg_grades:
                grades_sum += element
            avg = grades_sum / len(avg_grades)
            logger.info(avg)
            result_string += mark + ' '
        result_string += '= ' + str(round(avg, 2))
        result_string += '\n'
    logger.info(result_string)
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
                try:
                    result += lessonElement.select_one('.dnevnik-lesson__subject span').get_text('', True) + '  - '
                    home_task_element = lessonElement.select_one('.dnevnik-lesson__hometask .dnevnik-lesson__task')
                    if home_task_element:
                        result += '  ' + home_task_element.get_text('', True)
                except AttributeError:
                    logger.info(lessonElement.encode_contents())

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
    if not response.json()['result']:
        logger.info("Auth failed %s", response.json())
        return False

    logger.info("Auth success \nsession id = %s \n response from auth\n%s \n ", client.cookies['session_id'], response.text)

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
