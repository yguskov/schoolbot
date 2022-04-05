from bs4 import BeautifulSoup as bs
import requests

html_nso = requests.get('C:\Users\vangu\schoolbot\School.html')
soup_nso = bs(html_nso.text, 'html.parser')

mean_grades = []

for i in soup_nso.select('#g0_avg'):
    mn_gr = soup_nso.select('.cell')
    mean_grades.append(mn_gr)

print(mean_grades)
