# import os
# from googleapiclient.discovery import build
import json
from abc import ABC, abstractmethod
from typing import List, Any
import requests
import pathlib

path = pathlib.Path(__file__).parent
full_root = pathlib.Path(path, 'vacancies.json')


class API:
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def save_info(self):
        pass


class GetVacancy(API):

    def __init__(self, name: str):
        self.vac_name = name
        self.vac_list = []

    @property
    def get_vacancies(self):
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
            self.vac_list.append({"id": vac["id"],
                                  "name": vac["name"],
                                  "salary": vac["salary"],
                                  "url": vac["alternate_url"]})

            self.vac_list[s]['description'] = vac["snippet"]["requirement"] if "snippet" in vac and "requirement" in \
                                                                               vac["snippet"] else "без описания"
            if "area" in vac:
                self.vac_list[s]['city'] = vac["area"]["name"]
            else:
                self.vac_list[s]['city'] = "город не указан"
            s += 1

        return self.vac_list

    def save_info(self):
        if len(self.vac_list) == 0:
            return "Vacancy not found"
        else:
            with open(full_root, 'w', encoding='utf-8') as file:
                file.write(json.dumps(self.vac_list, indent=2, ensure_ascii=False))

    def __eq__(self, other):
        return True if (self.get_vacancies["salary"] == other.salary) else False

    def __le__(self, other):
        return True if (self.get_vacancies["salary"] <= other.salary) else False

    def __lt__(self, other):
        return True if (self.get_vacancies["salary"] < other.salary) else False

    def __ge__(self, other):
        return True if (self.get_vacancies["salary"] >= other.salary) else False

    def __gt__(self, other):
        return True if (self.get_vacancies["salary"] > other.salary) else False


class CertainVacancy(GetVacancy):

    def __init__(self, name: str, id_vac: int):
        super().__init__(name)
        self.id = id_vac

    def full_info(self):
        info_json = requests.get(f"https://api.hh.ru/vacancies/{self.id}")
        return json.dumps(info_json.json(), indent=2, ensure_ascii=False)


class SalaryVacancy(GetVacancy):

    # POLUCH_SALARY = 10
    def __init__(self, vac_name):
        super().__init__(vac_name)
        self.sort_salary = []
        self.url = ''
        self.desc = ''
        """проверка, указана ли зп, иначе = "Зарплата не указана" """

    def sorted_salary(self, top: int) -> list[Any]:
        """
           Выводит топ по зарплатам определенной профессии
        """
        if not self.get_vacancies:
            pass
        unsort_list = self.get_vacancies

        i = 0
        while i < len(unsort_list):
            if isinstance(unsort_list[i]["salary"], type(None)):
                unsort_list.remove(unsort_list[i])
                i -= 1
            if "from" in unsort_list[i]["salary"] and isinstance(unsort_list[i]["salary"]["from"], type(None)):
                del unsort_list[i]["salary"]["from"]
            i += 1

        def get_actual_salary(x):
            if isinstance(x["salary"], dict):
                return x["salary"]["from"] if "from" in x["salary"] else x["salary"]["to"]
            return x["salary"]

        self.sort_salary = sorted(unsort_list, key=lambda x: get_actual_salary(x), reverse=True)

        return self.sort_salary[:top]


#print(GetVacancy('python').get_vacancies)

# response = {
#     "area": 113,
# }
# req = requests.get('https://api.hh.ru/vacancies', response)
# data = req.content.decode()
# ans = json.loads(req.text)['items']
# print(ans)
#
# response = {
#     "area": 113,
# }
# req = requests.get('https://api.hh.ru/employers', response)
# data = req.content.decode()
# ans = json.loads(req.text)['items']
# print(ans)
# print(json.loads(data)['items'])
