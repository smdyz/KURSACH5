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

con = input('\n\nДля подключения к вашей базе данных необходимо вести ее данные в одну строку через 2 пробела.\n'
            'Не бойтесь они нигде не сохраняются... наверное:)\n'
            '(название БД, имя пользователя, пароль, порт *если стоит не дефолтный*) чтобы все сработало СОБЛЮДАЙТЕ '
            'ПОСЛЕДОВАТЕЛЬНОСТЬ\n')

con = con.split('  ')
try:
    con[3] = int(con[3])
    d = DBManager(con[0], con[1], con[2], con[3])
except:
    d = DBManager(con[0], con[1], con[2])
print(con)

try:
    while True:
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
except:
    print("введены неправильные данные для подключения к БД")
