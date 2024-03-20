from src.DBManager import DBManager

print('''Привет! 
Эта программа создает базу данных Postgresql
с краткой информацией о вакансиях и компаниях, полученной при помощи API hh.ru.
Для продолжения работы введите номер интересующего запроса\n''')

d = DBManager()
d.bd_data()

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
    4 - ввести свои данные для подключения к БД (обязательно для первого подключения)
    5 - вывести все компании
    6 - вывести все вакансии, предоставляемые полученными работодателями 
    7 - выйти\n''')

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
            con = input(
                '\n\nДля подключения к вашей базе данных необходимо вести ее данные в одну строку через 2 пробела.\n'
                'Не бойтесь они нигде не сохраняются... наверное:)\n'
                '(название БД, имя пользователя, пароль, порт *если стоит не дефолтный*) чтобы все сработало СОБЛЮДАЙТЕ'
                ' ПОСЛЕДОВАТЕЛЬНОСТЬ\n')
            with open('bd.txt', mode='w') as f:
                f.write(con)
            print('Для внесения изменений перезапустите программу')
        elif req == 5:
            d.get_companies_and_vacancies_count()
            d.print_employers()
        elif req == 6:
            d.get_all_vacancies()
            d.print_vacancies()
        elif req == 7:
            print('Завершение работы')
            break
        else:
            print('\n\nВведен некорректный номер запроса, попробуй еще раз... ')
            req = int(input())

        print('\nЕсли интересует что-то еще, можете ввести еще один запрос, либо выйти (6)')
except:
    print("введены неправильные данные для подключения к БД")
