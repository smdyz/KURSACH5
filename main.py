from src.DBManager import DBManager

print('''Привет! 
Эта программа создает базу данных Postgresql
с краткой информацией о вакансиях и компаниях, полученной при помощи API hh.ru.
Для продолжения работы введите номер интересующего запроса\n\n''')

try:
    with open('bd.txt', mode='r') as f:
        con = f.read()
        con = con.split('  ')
        if len(con) == 4:
            con[3] = int(con[3])
            d = DBManager(con[0], con[1], con[2], con[3])
        elif len(con) == 3:
            d = DBManager(con[0], con[1], con[2])
except:
    print("нт")

try:
    print('''1 - создать базу данных с заполнением данными с сайта hh.ru
2 - получить среднюю зарплату по полученным вакансиям
3 - получить вакансии с зарплатой выше средней
4 - найти вакансии с ключевым словом в названии
5 - ввести свои данные для подключения к БД (обязательно для первого подключения)
6 - вывести все компании
7 - вывести все вакансии, предоставляемые полученными работодателями 
8 - выйти\n''')

    while True:
        req = int(input())
        if req == 1:
            d.create_tables()
            d.to_postgresql("employers", d.get_companies_and_vacancies_count())
            d.get_all_vacancies()
            d.to_postgresql('vacancies', d.vacancies)
        elif req == 2:
            d.get_avg_salary()
        elif req == 3:
            d.get_vacancies_with_higher_salary()
        elif req == 4:
            try:
                key_word = input('\nВведите ключевое слово: ')
                d.get_vacancies_with_keyword(key_word)
            except:
                print('\nВакансии не найдены')
        elif req == 5:
            con = input(
                '\n\nДля подключения к вашей базе данных необходимо вести ее данные в одну строку через 2 пробела.\n'
                'Не бойтесь они нигде не сохраняются... наверное:)\n'
                '(название БД, имя пользователя, пароль, порт *если стоит не дефолтный*) чтобы все сработало СОБЛЮДАЙТЕ'
                ' ПОСЛЕДОВАТЕЛЬНОСТЬ\n')
            with open('bd.txt', mode='w') as f:
                f.write(con)
        elif req == 6:
            d.get_companies_and_vacancies_count()
            d.print_employers()
        elif req == 7:
            d.get_all_vacancies()
            d.print_vacancies()
        elif req == 8:
            print('Завершение работы')
            break
        else:
            print('\n\nВведен некорректный номер запроса, попробуй еще раз... ')
            req = int(input())

        print('\nЕсли интересует что-то еще, можете ввести еще один запрос, либо выйти (6)')
except:
    print("введены неправильные данные для подключения к БД")
