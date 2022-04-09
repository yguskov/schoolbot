import json
import os
import requests
import logging

logger = logging.getLogger(__name__)
session_data = {}

def read_grades() -> str:
    global session_data
    cookies = {'school_domain': 'nso1613660760', 'schdomain': 'nso1613660760', 'session_id': session_data['session_id']}

    client = requests.Session()

    response = client.get('https://school.nso.ru/journal-student-grades-action/u.2169', cookies=cookies)
    return response.text

def auth(login: str, password: str) -> bool:

    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
    }

    cookies = {'school_domain': 'nso1613660760', 'schdomain': 'nso1613660760'} # , 'session_id': 'e76f5e354dbeac4cf77ca5e2f7b47ca0'

    # data = "email=yguskov@rssystems.ru&password=ggm"
    # data = "username="+login+"&password="+password+"&return_uri=/"
    data = {'username': login, 'password': password}
#   data = "username=taliguskova&password=011294Kj&return_uri=/"

    logger.info(data)

    client = requests.Session()

    response = client.post('https://school.nso.ru/ajaxauthorize', data)
    # response = client.get('https://school.nso.ru/journal-student-grades-action/u.2169', cookies=cookies)

    logger.info("Auth success \nsession id = %s \n response from auth\n%s \n ", client.cookies['session_id'], response.text)

    chat_id = os.environ['chat_id']

    # save session id to file
    global session_data
    session_data = {'chat_id': chat_id, 'session_id': client.cookies['session_id']}

    with open('data/' + chat_id + '.json', 'w') as outfile:
        outfile.write(json.dumps(session_data))

    return True


#     response = client.post('http://pubrgg.nsu.ru/user/login', headers=headers, data=data)
    response = client.post('https://school.nso.ru/ajaxauthorize', headers=headers,  cookies=cookies, data=data)
#     logger.info("Authorize response %s \n ", response.text)

    response = client.get('https://school.nso.ru/journal-student-grades-action/u.2169')

#     logger.info("Grades response %s \n ", response.text)

    return True

