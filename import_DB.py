import mysql.connector
import csv

def create_companies_DB():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ErhCthdbC_2006",
            database="test_DB"
        )
        cursor = mydb.cursor()
        with open("companies_csv.csv", "r", encoding="utf-8", newline="") as csv_file:
            reader = csv.reader(csv_file)
            headers = next(reader)
            data = list(reader)
            print()
            print("Создается таблица со следующим заголовком: {}".format(headers))
            print(data[0], data[-1])
        count = 0
        for line in data:
            sql_insert_query = """INSERT INTO companies
                              (company_name, company_action, industry, country)
                              VALUES
                              (%s, %s, %s, %s);"""
            cursor.execute(sql_insert_query, line)
            mydb.commit()
            print("Строка :", line, " добавлена в БД")
            count += 1
        print("Добавлено {} строк".format(count))
        cursor.close()

    except mysql.connector.Error as error:
        print("Ошибка при работе с MySQL", error)
    finally:
        if mydb:
            mydb.close()
            print("Соединение с MySQL закрыто")

def find_companies(company_name):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ErhCthdbC_2006",
            database="test_DB"
        )
        cursor = mydb.cursor()
        sql_select_query = """SELECT company_action FROM companies WHERE company_name = %s;"""
        cursor.execute(sql_select_query, (company_name,))
        result = cursor.fetchone()
        cursor.close()
        return result

    except mysql.connector.Error as error:
        print("Error at work at MySQL", error)
    finally:
        if mydb:
            mydb.close()
            print("Connection with MySQL closed")