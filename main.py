from src.DBManager import DBManager
from src.DBManager import for_API

print('''Привет! 
Эта программа создает базу данных Postgresql
с краткой информацией о вакансиях и компаниях, полученной при помощи API hh.ru.
Для продолжения работы введите номер интересующего запроса\n''')

d = DBManager()

if d.check() is True:
    print('Создаем базу данных подождите немного...\n')
    d.create_tables()
    d.get_companies_and_vacancies_count()
    d.get_all_vacancies()
    d.to_postgresql('employers')
    d.to_postgresql('vacancies')

try:
    print('''    1 - получить среднюю зарплату по полученным вакансиям
    2 - получить вакансии с зарплатой выше средней
    3 - найти вакансии с ключевым словом в названии
    4 - вывести все компании
    5 - вывести все вакансии, предоставляемые полученными работодателями 
    6 - выйти\n''')

    while True:
        req = int(input())
        if req == 1:
            d.get_avg_salary()
        elif req == 2:
            d.get_vacancies_with_higher_salary()
        elif req == 3:
            try:
                key_word = input('\nВведите ключевое слово: ')
                d.get_vacancies_with_keyword(key_word)
            except:
                print('\nВакансии не найдены')
        elif req == 4:
            d.print_employers()
        elif req == 5:
            d.print_vacancies()
        elif req == 6:
            print('Завершение работы')
            break
        else:
            print('\n\nВведен некорректный номер запроса, попробуй еще раз... ')
            req = int(input())

        print('\nЕсли интересует что-то еще, можете ввести еще один запрос, либо выйти (6)')
except:
    print("введены неправильные данные для подключения к БД")
