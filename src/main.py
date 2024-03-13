from src.DBManager import DBManager

print('''Привет! 
Эта программа создает базу данных Postgresql
с краткой информацией о вакансиях и компаниях, полученной при помощи API hh.ru.
Для продолжения работы введите номер интересующего запроса\n\n''')

req = int(input('''1 - создать базу данных с заполнением данными с сайта hh.ru
2 - получить среднюю зарплату по полученным вакансиям
3 - получить вакансию с самой высокой зарплатой
4 - найти вакансии с ключевым словом в названии
5 - выйти\n'''))

while True:
    d = DBManager()
    if req == 1:
        d.create_tables()
        d.to_postgresql("employers", d.get_companies_and_vacancies_count)
        d.get_all_vacancies()
        d.to_postgresql('vacancies', d.vacancies)
        break
    elif req == 2:
        d.get_avg_salary()
        break
    elif req == 3:
        d.get_vacancies_with_higher_salary()
        break
    elif req == 4:
        key_word = input('\n\nВведите ключевое слово: ')
        d.get_vacancies_with_keyword(key_word)
        break
    elif req == 5:
        break
    else:
        print('\n\nВведен некорректный номер запроса, попробуй еще раз... ')
        req = int(input())
