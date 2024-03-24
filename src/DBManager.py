import psycopg2
import json
import requests
from src import database


class for_API:
    """
    Класс for_API создан для получения данных о компаниях и вакансиях с сайта hh.ru посредством API ключа.
    """

    def __init__(self):
        self.vacancies = []
        self.employers = []

    def get_companies_and_vacancies_count(self):
        i = 1
        j = 15
        while i < j:
            req = requests.get('https://api.hh.ru/employers/' + str(i))
            data = req.content.decode()
            req.close()
            jo = json.loads(data)
            try:
                if jo['open_vacancies'] > 0 and jo['open_vacancies'] is not None:
                    self.employers.append([jo['id'], jo['name'],
                                           jo['open_vacancies']])
                    i += 1
                    continue
                i += 1
                j += 1
            except:
                i += 1
                j += 1
        req = requests.get('https://api.hh.ru/employers/' + str(1740))
        data = req.content.decode()
        req.close()
        jo = json.loads(data)
        self.employers.append([jo['id'], jo['name'], jo['open_vacancies']])
        return self.employers

    def get_all_vacancies(self):
        params = {
            'employer_id': [],
            'area': 113,
            'per_page': 100  # Кол-во вакансий на 1 странице
        }
        for i in self.employers:
            params['employer_id'].append(i[0])
        for page in range(0, 10):
            params['page'] = page
            req = requests.get('https://api.hh.ru/vacancies', params)
            data = req.content.decode()
            req.close()
            data = json.loads(data)['items']
            for i in data:
                try:
                    if i['salary']['from'] is None:
                        self.vacancies.append(
                            [i['name'], i['apply_alternate_url'], i['salary']['to'], i['employer']['id']])
                    else:
                        self.vacancies.append(
                            [i['name'], i['apply_alternate_url'], i['salary']['from'], i['employer']['id']])
                except:
                    self.vacancies.append([i['name'], i['apply_alternate_url'], i['salary'], i['employer']['id']])
        return self.vacancies


class DBManager(for_API):
    """
    Класс DBManager создан для работы с базой данных, основанной на данных, полученных с сайта hh.ru.
    В нем реализована централизованное хранение request'ов в базе данных Postgresql.

    Методы:
    create_tables - создание 2 таблиц для работодателей и вакансий
    to_postgresql - заполнение таблиц полученными данными
    get_avg_salary - расчет средней зарплаты
    get_vacancies_with_higher_salary - вывод самой высокой зарплаты
    get_vacancies_with_keyword - поиск по ключевому слову
    """

    def __init__(self):
        super().__init__()
        self.db = database.database
        self.user = database.user
        self.pswd = database.password
        self.port = 5432
        self.connect = None

    def con(self):
        self.connect = psycopg2.connect(
            database=self.db,
            user=self.user,
            password=self.pswd,
            port=self.port
        )

    def create_tables(self):
        self.con()
        try:
            with self.connect:
                with self.connect.cursor() as cur:
                    cur.execute('''drop table if exists vacancies;
                                drop table if exists employers;
                                create table vacancies (
                                    vac_name varchar NOT NULL,
                                    url varchar NOT NULL,
                                    salary int,
                                    emp_id int
                                );
                                
                                create table employers (
                                    emp_id int unique NOT NULL,
                                    emp_name varchar NOT NULL,
                                    emp_open_vac int
                                );''')
        finally:
            self.connect.close()

    def to_postgresql(self, tab_name):
        # try:
        self.con()
        with self.connect:
            with self.connect.cursor() as cur:
                if tab_name == 'vacancies':
                    for tabs_info in self.vacancies:
                        cur.execute(f'insert into {tab_name} values (%s, %s, %s, %s)',
                                    (tabs_info[0], tabs_info[1], tabs_info[2], tabs_info[3]))
                elif tab_name == 'employers':
                    for tabs_info in self.employers:
                        cur.execute(f'insert into {tab_name} values (%s, %s, %s)',
                                    (tabs_info[0], tabs_info[1], tabs_info[2]))
        # finally:
        self.connect.close()

    def get_avg_salary(self):
        self.con()
        try:
            with self.connect:
                with self.connect.cursor() as cur:
                    cur.execute('select avg(salary) from vacancies;')
                    rows = cur.fetchall()
                    for row in rows:
                        avg = float(row[0])
                        print(round(avg, 2))
        finally:
            self.connect.close()

    def get_vacancies_with_higher_salary(self):
        self.con()
        try:
            with self.connect:
                with self.connect.cursor() as cur:
                    cur.execute('SELECT vac_name, salary, url FROM vacancies WHERE salary > (SELECT AVG(salary) FROM '
                                'vacancies);')
                    rows = cur.fetchall()
                    for row in rows:
                        print(f'''Название вакансии - {row[0]}
Зарплата - {row[1]}
Ссылка - {row[2]}\n''')
        finally:
            self.connect.close()

    def get_vacancies_with_keyword(self, key_word):
        self.con()
        try:
            with self.connect:
                with self.connect.cursor() as cur:
                    cur.execute("SELECT * FROM vacancies WHERE vac_name LIKE %s", (f'%{key_word}%',))
                    rows = cur.fetchall()
                    for row in rows:
                        print(row)
        finally:
            self.connect.close()

    def check(self):
        try:
            self.con()
            with self.connect:
                with self.connect.cursor() as cur:
                    cur.execute("SELECT * FROM vacancies")
                    rows = cur.fetchall()
                    if len(rows) > 0:
                        return False
                    return True
        except:
            return True
        finally:
            self.connect.close()

    def print_employers(self) -> None:
        self.con()
        try:
            with self.connect:
                with self.connect.cursor() as cur:
                    cur.execute("SELECT * FROM employers")
                    rows = cur.fetchall()
                    for row in rows:
                        print(f'''id - {row[0]}
Название компании - {row[1]}
Количество открытых вакансий - {row[2]}\n''')
        finally:
            self.connect.close()

    def print_vacancies(self) -> None:
        self.con()
        try:
            with self.connect:
                with self.connect.cursor() as cur:
                    cur.execute("SELECT * FROM vacancies")
                    rows = cur.fetchall()
                    for row in rows:
                        print(f'''Название вакансии - {row[0]}
Ссылка - {row[1]}
Зарплата - {row[2]}
id работодателя - {row[3]}\n''')
        finally:
            self.connect.close()
