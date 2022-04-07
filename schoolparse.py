from bs4 import BeautifulSoup as bs

from pathlib import Path

# html_nso = requests.get('https://school.nso.ru/journal-student-grades-action/u.2169')

import codecs
fileObj = codecs.open("grades_example.html", "r", "utf_8_sig")
html_nso = fileObj.read() # или читайте по строке
fileObj.close()

# html_nso = Path('grades_example.html').read_text()

soup_nso = bs(html_nso, 'html.parser')

grades = dict()

for domElement in soup_nso.select('div[mark_date]'):
    if domElement.get('mark_date') != "":
        if domElement.get('name') in grades:
            grades[domElement.get('name')][domElement.get('mark_date')] = domElement.get_text('', True)
        else:
            grades[domElement.get('name')] = dict()
    # mn_gr = soup_nso.select('.cell')
    # mean_grades.append(mn_gr)

resultString = ''
for subject, marks in grades.items():
    # print(subject, end=' : ')
    resultString += subject
    resultString += ': '
    for date, mark in marks.items():
        resultString += mark + ' '
        # print(mark, end=' ')
    resultString += '\n'

print(resultString)

