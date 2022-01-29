import requests
import logging

logger = logging.getLogger(__name__)

def auth(login: str, password: str) -> bool:

    headers = {
        'Content-type': 'application/x-www-form-urlencoded',
    }

    cookies = {'school_domain': 'nso1613660760', 'schdomain': 'nso1613660760', 'session_id': 'e76f5e354dbeac4cf77ca5e2f7b47ca0'}

    data = "email=yguskov@rssystems.ru&password=ggm"
    data = "username=taliguskova&password=011294Kj&return_uri=/"
#     data = '{"text":"Hello, World!"}'

    client = requests.Session()

    response = client.get('https://school.nso.ru/journal-student-grades-action/u.2169', cookies=cookies)

    logger.info("Grades response %s \n ", response.text)
#     print(client.cookies['session_id'])

    return True


#     response = client.post('http://pubrgg.nsu.ru/user/login', headers=headers, data=data)
    response = client.post('https://school.nso.ru/ajaxauthorize', headers=headers,  cookies=cookies, data=data)
#     logger.info("Authorize response %s \n ", response.text)
    print(client.cookies['session_id'])

    response = client.get('https://school.nso.ru/journal-student-grades-action/u.2169')

#     logger.info("Grades response %s \n ", response.text)
    print(client.cookies['session_id'])

    return True
