from bs4 import BeautifulSoup as bs
import requests

from pathlib import Path

# html_nso = requests.get('https://school.nso.ru/journal-student-grades-action/u.2169')
html_nso = Path('grades_example.html').read_text()

soup_nso = bs(html_nso, 'html.parser')

grades = dict()
print(len(soup_nso.select('div[mark_date]')))
for domElement in soup_nso.select('div[mark_date]'):
    if domElement.get('mark_date') != "":
        if domElement.get('name') in grades:
            grades[domElement.get('name')][domElement.get('mark_date')] = domElement.get_text('', True)
        else:
            grades[domElement.get('name')] = dict()
    # mn_gr = soup_nso.select('.cell')
    # mean_grades.append(mn_gr)

for subject in grades:
    print(grades[subject])

