import psycopg2


class DBManager:
    """ класс DBManager для работы с данными в БД. """

    def __init__(self, dbname: str, params: dict) -> None:
        self.conn = psycopg2.connect(dbname=dbname, **params)
        self.dbname = dbname
        self.params = params

    def get_companies_and_vacancies_count(self):
        """
        получает список всех компаний и количество вакансий у каждой компании.
        :return: список всех компаний и количество вакансий у каждой компании.
        """
        with psycopg2.connect(dbname=self.dbname, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        SELECT company.employer_id, company.employer_name, 
                        COUNT(vacancies.employer_id) AS vacancies_count
                        FROM company
                        LEFT JOIN vacancies USING(employer_id)
                        GROUP BY company.employer_id;
                    """
                )
                rows = cur.fetchall()
                return rows

    def get_all_vacancies(self):
        """
        получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
        :return: список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
        """
        with psycopg2.connect(dbname=self.dbname, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        SELECT company.employer_name, vacancies.vacancy_name, 
                        CONCAT_WS('-', vacancies.salary_from, vacancies.salary_to) AS salary,vacancies.vacancy_url
                        FROM vacancies
                        LEFT JOIN company USING(employer_id)
                        ORDER BY company.employer_name
                    """
                )
                rows = cur.fetchall()
                return rows

    def get_avg_salary(self):
        """
        получает среднюю зарплату по вакансиям.
        :return: среднюю зарплату по вакансиям.
        """
        with psycopg2.connect(dbname=self.dbname, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        SELECT (AVG(vacancies.salary_from) + AVG(vacancies.salary_to)) / 2 AS avg_salary
                        FROM vacancies
                    """
                )
                rows = cur.fetchall()
                return rows

    def get_vacancies_with_higher_salary(self):
        """
        получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return: список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        with psycopg2.connect(dbname=self.dbname, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        SELECT * FROM vacancies
                        WHERE (salary_from + salary_to) / 2 > 
                        (SELECT (AVG(salary_from) + AVG(salary_to)) / 2 FROM vacancies)
                    """
                )
                rows = cur.fetchall()
                return rows

    def get_vacancies_with_keyword(self, keyword: str):
        """
        получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        :param keyword: ключевое слово для поиска в названии вакансии
        :return: список всех вакансий, в названии которых содержатся переданные в метод слова
        """
        with psycopg2.connect(dbname=self.dbname, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                        SELECT * FROM vacancies
                        WHERE LOWER(vacancy_name) LIKE '%{keyword}%'
                     """
                )
                rows = cur.fetchall()
                return rows
