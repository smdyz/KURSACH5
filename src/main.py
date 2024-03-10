import time
import json
import requests
from src.DBManager import DBManager


params = {
    'employer_id': [6, 13, 15, 1740],
    'area': 113,         # Поиск в зоне
    'per_page': 100       # Кол-во вакансий на 1 странице
}
req = requests.get('https://api.hh.ru/vacancies', params)
data = req.content.decode()
req.close()
data = json.loads(data)['items']
#print(data)
for i in data:
    try:
        print([i['name'], i['employer']['name'], i['apply_alternate_url']])
    except:
        print([i['name'], i['employer']['name'], '=============================================================='])

man = DBManager()
print(man.get_companies_and_vacancies_count())


# create table employers(
# 	id int unique,
# 	company_name varchar,
# 	open_vacancies int,
# 	title varchar,
# 	notes text,
# );
#
# create table vacancies(
# 	id int unique,
# 	vacancy_name varchar,
# 	salary int,
# 	city varchar,
# 	description text,
# );
