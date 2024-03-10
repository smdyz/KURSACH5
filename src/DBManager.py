import psycopg2
import classes
import json
import requests


class DBManager:

    def __init__(self):
        self.vacancies = []
        self.employers = []

    @property
    def get_companies_and_vacancies_count(self):
        # del_char = ['<p>', '<em>', '', '', '', '', '', '', '', '', '']
        req = requests.get('https://api.hh.ru/employers', {'area': 113})
        data = req.content.decode()
        req.close()
        #count_of_employers = json.loads(data)['found']
        self.employers = []
        i = 1
        j = 15
        print(j)
        while i < j:
            req = requests.get('https://api.hh.ru/employers/' + str(i))
            data = req.content.decode()
            req.close()
            jo = json.loads(data)
            try:
                if jo['open_vacancies'] > 0 and jo['open_vacancies'] is not None:
                    self.employers.append([jo['id'], jo['name'], jo['open_vacancies']])#, jsObj['alternate_url'], jsObj['description']])
                    print([jo['id'], jo['name'], jo['open_vacancies'], jo['alternate_url'], jo['description']])
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
        #self.vacancies = classes.GetVacancy
        self.get_companies_and_vacancies_count()

        response = {
            "area": 113,
            "per_page": 100
        }
        answer = requests.get("https://api.hh.ru/vacancies", response)

        if answer == "" or answer == [] or answer is None:
            return []

        vacs = json.loads(answer.text)['items']
        s = 0
        for vac in vacs:
            self.vacancies.append([vac["id"], vac["name"], vac["salary"], vac["alternate_url"]])

            self.vacancies[s].append(vac["snippet"]["requirement"]) if "snippet" in vac and "requirement" in \
                                                                               vac["snippet"] else "без описания"
            if "area" in vac:
                self.vacancies[s].append(vac["area"]["name"])
            else:
                self.vacancies[s]['city'] = "город не указан"
            s += 1

        return self.vacancies

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass