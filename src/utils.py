from typing import Any
import psycopg2


def create_database(database_name: str, params: dict) -> None:
    '''
    Создание базы данных и таблиц для сохранения данных о каналах и видео.
    :param database_name: название базы данных для создания
    :param params: Параметры для подключения к базе данных
    :return: None
    '''

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE company (
                employer_id INT,
                employer_name VARCHAR(255) NOT NULL,
                type VARCHAR(255),
                employer_url TEXT,
                site_url TEXT,
                CONSTRAINT pk_company_employer_id PRIMARY KEY (employer_id)
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id INT,
                vacancy_name VARCHAR(255) NOT NULL,
                date_published DATE,
                salary_from INTEGER,
                salary_to INTEGER,
                valute VARCHAR(20),
                type_of_work VARCHAR(255),
                experience VARCHAR(255),
                vacancy_url TEXT,
                employer_id INT,
                CONSTRAINT pk_vacancies_vacancy_id PRIMARY KEY(vacancy_id),
                CONSTRAINT fk_vacancies_employer_id FOREIGN KEY(employer_id) REFERENCES company(employer_id)
            )
        """)
    conn.commit()
    conn.close()


def save_data_to_database(company_data: list[dict[str, Any]], vacancy_data: list[dict[str, Any]],
                          database_name: str, params: dict) -> None:
    '''
    Сохранение данных о работодателях и их вакансиях в базу данных.
    :param company_data: список словарей с данными компаний
    :param vacancy_data: список словарей с данными вакансий
    :param database_name: название базы данных для подключения
    :param params: Параметры для подключения к базе данных
    :return: None
    '''

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for company in company_data:
            cur.execute(
                """
                INSERT INTO company (employer_id, employer_name, type, employer_url, site_url)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (company['employer_id'], company['employer_name'], company['type'],
                 company['employer_url'], company['site_url'])
            )

    conn.commit()

    with conn.cursor() as cur:
        for vacancy in vacancy_data:
            cur.execute(
                """
                    INSERT INTO vacancies (vacancy_id, vacancy_name, date_published, salary_from, 
                    salary_to, valute, type_of_work, experience, vacancy_url, employer_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (vacancy['vacancy_id'], vacancy['vacancy_name'], vacancy['date_published'], vacancy['salary_from'],
                 vacancy['salary_to'], vacancy['salary_currency'], vacancy['type_of_work'], vacancy['experience'],
                 vacancy['link'], vacancy['employer_id'])
            )

    conn.commit()
    conn.close()
