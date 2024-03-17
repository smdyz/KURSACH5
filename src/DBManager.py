import psycopg2
import json
import requests


class DBManager:
    """
    Класс DBManager создан для получения данных о компаниях и вакансиях с сайта hh.ru посредством API ключа.
    В нем реализована централизованное хранение request'ов в базе данных Postgresql.

    Переменные:
    self.vacancies - список вакансий, включающий ее наименование, ссылку, зарплату и id работодателя
    self.employers - список компаний (работодателей), включающий его id, название и количество открытых вакансий

    Методы:
    create_tables - создание 2 таблиц для работодателей и вакансий
    to_postgresql - заполнение таблиц полученными данными
    get_companies_and_vacancies_count - получение по API краткой информации о компаниях
    get_all_vacancies - получение по API краткой информации о вакансиях
    get_avg_salary - расчет средней зарплаты
    get_vacancies_with_higher_salary - вывод самой высокой зарплаты
    get_vacancies_with_keyword - поиск по ключевому слову
    """

    def __init__(self, db: str, user: str, pswd: str, port=5432):
        self.vacancies = []
        self.employers = []
        self.db = db
        self.user = user
        self.pswd = pswd
        if isinstance(port, int):
            self.port = port

    def create_tables(self):
        connection = psycopg2.connect(
            database=self.db,
            user=self.user,
            password=self.pswd,
            port=self.port
        )

        try:
            with connection:
                with connection.cursor() as cur:
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
            connection.close()

    def to_postgresql(self, tab_name: str, tab: list):
        connection = psycopg2.connect(
            database=self.db,
            user=self.user,
            password=self.pswd,
            port=self.port
        )

        try:
            with connection:
                with connection.cursor() as cur:
                    for tabs_info in tab:
                        if len(tabs_info) == 3:
                            cur.execute(f'insert into {tab_name} values (%s, %s, %s)',
                                        (tabs_info[0], tabs_info[1], tabs_info[2]))
                        if len(tabs_info) == 4:
                            cur.execute(f'insert into {tab_name} values (%s, %s, %s, %s)',
                                        (tabs_info[0], tabs_info[1], tabs_info[2], tabs_info[3]))
        finally:
            connection.close()

    @property
    def get_companies_and_vacancies_count(self):
        # req = requests.get('https://api.hh.ru/employers', {'area': 113})
        # data = req.content.decode()
        # req.close()
        # count_of_employers = json.loads(data)['found']
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

    def get_avg_salary(self):
        connection = psycopg2.connect(
            database=self.db,
            user=self.user,
            password=self.pswd,
            port=self.port
        )

        try:
            with connection:
                with connection.cursor() as cur:
                    cur.execute('select avg(salary) from vacancies;')
                    rows = cur.fetchall()
                    for row in rows:
                        avg = float(str(row)[10:-4])
                        print(round(avg, 2))
        finally:
            connection.close()

    def get_vacancies_with_higher_salary(self):
        connection = psycopg2.connect(
            database=self.db,
            user=self.user,
            password=self.pswd,
            port=self.port
        )

        try:
            with connection:
                with connection.cursor() as cur:
                    cur.execute('SELECT MAX(salary) FROM vacancies;')
                    rows = cur.fetchall()
                    for row in rows:
                        print(int(str(row)[1:-2]))
        finally:
            connection.close()

    def get_vacancies_with_keyword(self, key_word):
        connection = psycopg2.connect(
            database=self.db,
            user=self.user,
            password=self.pswd,
            port=self.port
        )

        try:
            with connection:
                with connection.cursor() as cur:
                    cur.execute("SELECT * FROM vacancies WHERE vac_name LIKE %s", (f'%{key_word}%',))
                    rows = cur.fetchall()
                    for row in rows:
                        print(row)
        finally:
            connection.close()
