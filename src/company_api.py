from src.errors import ParsingError
import requests


class HHCompany:
    """ Класс для получения данные о работодателях с Api hh.ru """

    @classmethod
    def get_company_data(cls, company_ids: list) -> list[dict[str]]:
        """
        Получает данные о работодателях с сайта в формате json словарей
        :param company_ids: список id компаний
        :return: список данные о работодателях в формате json словарей
        """
        company_data = []

        for company_id in company_ids:
            response = requests.get(f"https://api.hh.ru/employers/{company_id}")
            try:
                if response.status_code == 200:
                    data = response.json()
                    company_data.append(data)
                else:
                    # В случае ошибки запроса будет выведено сообщение
                    raise ParsingError(response.status_code)
            except ParsingError as ex:
                print(f"Ошибка в запросе код: {ex.key_error}")

        return company_data

    @classmethod
    def package_company_data(cls, company_data: list[dict[str]]) -> list[dict[str]]:
        """
        получает список со всеми данными работодателей с Api и складывает в список класса
        :param company_data: Список с данными работодателей
        :return: список сортированных данных компаний
        """
        companys = []

        try:
            for company in company_data:
                # Создание списка для записи шаблона данных работодателей в файл

                sorted_company = {
                    "employer_id": company['id'],
                    "employer_name": company['name'],
                    "employer_url": company['alternate_url'],
                    "type": company['type'],
                    "site_url": company['site_url'] if company['site_url'] else None
                }
                companys.append(sorted_company)

        except TypeError as ex:
            print(f"Тип данных для записи шаблона не корректен : {ex}")

        return companys
