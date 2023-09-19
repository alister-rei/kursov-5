from config import config
from utils import create_database, save_data_to_database
from vacancy_api import HHVacancy
from company_api import HHCompany
from db_manager import DBManager

# constant
DBNAME = "kursov5"
KEYWORD = "python"
PARAMS = config()
COMPANY_IDS = [2725721, 2633363, 1122462, 51167, 460838, 5061389, 1993194, 67611, 143439, 10025564]


def main():
    vacancies = HHVacancy.get_vacancies(COMPANY_IDS)
    sort_vacancies = HHVacancy.package_vacancies(vacancies)

    companys = HHCompany.get_company_data(COMPANY_IDS)
    sort_companys = HHCompany.package_company_data(companys)

    create_database(DBNAME, PARAMS)
    save_data_to_database(sort_companys, sort_vacancies, DBNAME, PARAMS)

    while True:
        print(
            """
        0 - 
        1 - получает список всех компаний и количество вакансий у каждой компании.
        2 - получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
        3 - получает среднюю зарплату по вакансиям.
        4 - получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        5 - получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
            """
        )
        user_choice = int(input("f"))
        if user_choice == 0:
            break

        elif user_choice == 1:
            dbmanager = DBManager(DBNAME, PARAMS)
            rows = dbmanager.get_companies_and_vacancies_count()
            for row in rows:
                print(row)

        elif user_choice == 2:
            dbmanager = DBManager(DBNAME, PARAMS)
            rows = dbmanager.get_all_vacancies()
            for row in rows:
                print(row)

        elif user_choice == 3:
            dbmanager = DBManager(DBNAME, PARAMS)
            rows = dbmanager.get_avg_salary()
            for row in rows:
                print(row)

        elif user_choice == 4:
            dbmanager = DBManager(DBNAME, PARAMS)
            rows = dbmanager.get_vacancies_with_higher_salary()
            for row in rows:
                print(row)

        elif user_choice == 5:
            dbmanager = DBManager(DBNAME, PARAMS)
            rows = dbmanager.get_vacancies_with_keyword(KEYWORD)
            for row in rows:
                print(row)

        else:
            print("not comand")

if __name__ == "__main__":
    main()
