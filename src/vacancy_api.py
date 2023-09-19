from errors import ParsingError
from datetime import datetime
import requests


class HHVacancy:
    """ Класс для получения вакансий с Api hh.ru """

    @classmethod
    def get_vacancies(cls, company_ids: list) -> list[dict[str]]:
        """
        Получает вакансии с сайта в формате json словарей
        :param company_ids: список id компаний по которым проводится поиск
        :return: список вокансий в формате json словарей
        """
        vacancies = []

        for company_id in company_ids:
            params = {
                "employer_id": company_id,
                "area": 2,
                "per_page": 100
            }
            response = requests.get("https://api.hh.ru/vacancies", params=params)
            try:
                if response.status_code == 200:
                    data = response.json()
                    vacancies.extend(data['items'])
                else:
                    # В случае ошибки запроса будет выведено сообщение
                    raise ParsingError(response.status_code)
            except ParsingError as ex:
                print(f"Ошибка в запросе код: {ex.key_error}")

        return vacancies

    @classmethod
    def package_vacancies(cls, data_vacancies: list[dict[str]]) -> list[dict[str]]:
        """
        получает список со всеми данными вакансий с Api и складывает в список класса
        :param data_vacancies: Список с данными вакансий
        :return: список сортированных данных вакансий
        """
        vacancies = []

        try:
            for vacancy in data_vacancies:
                # Создание списка для записи шаблона данных профессии в файл
                date = datetime.strptime(vacancy['published_at'], "%Y-%m-%dT%H:%M:%S%z").strftime("%Y-%m-%d %H:%M")
                salary_from = None
                salary_to = None
                salary_currency = None
                if not vacancy['salary'] is None:
                    if vacancy['salary']['from']:
                        salary_from = vacancy['salary']['from']
                    if vacancy['salary']['to']:
                        salary_to = vacancy['salary']['to']
                    if vacancy['salary']['currency']:
                        salary_currency = vacancy['salary']['currency']

                    if vacancy['salary']['currency'] not in ['RUR', None]:
                        # получаем коэффициент для конвертации валюты в рубли
                        get_valutes = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
                        valute = get_valutes.json()
                        rate = int(valute['Valute'][vacancy['salary']['currency']]['Value'])
                        salary_from = str(int(vacancy['salary']['from']) * rate) if vacancy['salary']['from'] else None
                        salary_to = str(int(vacancy['salary']['to']) * rate) if vacancy['salary']['to'] else None

                sorted_vacancy = {
                    "vacancy_id": vacancy['id'],
                    "vacancy_name": vacancy['name'],
                    "date_published": date,
                    "salary_from": salary_from,
                    "salary_to": salary_to,
                    "salary_currency": salary_currency,
                    "type_of_work": vacancy['employment']['name'],
                    "experience": vacancy['experience']['name'],
                    "requirement": vacancy['snippet']['requirement'],
                    "link": vacancy['alternate_url'],
                    "employer_id": vacancy['employer']['id']
                }
                vacancies.append(sorted_vacancy)

        except TypeError as ex:
            print(f"Тип данных для записи шаблона не корректен : {ex}")

        return vacancies
