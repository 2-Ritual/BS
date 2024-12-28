import mysql.connector
import os
from mysql.connector import Error


MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '1234')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'price_cmp')


def connect_to_db():
    try:
        db = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        if db.is_connected():
            print("成功连接到 MySQL 数据库")
            return db
    except Error as e:
        print("连接失败: ", e)
        return None


def insert_data_user(connection, username, password, email):
    cursor = connection.cursor()
    try:
        sql_insert_query = """INSERT INTO backend_user (username, password, email, reminder_1, reminder_2, reminder_3, reminder_4, reminder_5) VALUES (%s, %s, %s, 0, 0, 0, 0, 0)"""
        cursor.execute(sql_insert_query, (username, password, email))
        connection.commit()
    except Error as e:
        print(f"插入数据失败: {e}")
    finally:
        cursor.close()


def insert_data_product(connection, product_name, price_1, price_2, price_3, price_4, price_5, price_6, price_7, price_8, price_9, price_10, price_11, price_12, product_url, image, origin):
    cursor = connection.cursor()
    try:
        sql_insert_query = """INSERT INTO backend_product (product_name, price_1, price_2, price_3, price_4, price_5, price_6, price_7, price_8,
                                                            price_9, price_10, price_11, price_12, product_url, image, origin)
                                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql_insert_query, (product_name, price_1, price_2, price_3, price_4, price_5,
                                          price_6, price_7, price_8, price_9, price_10, price_11, price_12, product_url, image, origin))

        connection.commit()
    except Error as e:
        print(f"插入数据失败: {e}")
    finally:
        cursor.close()


if __name__ == "__main__":
    conn = connect_to_db()
    if conn:
        # insert_data_user(conn, 'usr1', '4d4f26369171994f3a46776ee2d88494fb9955800a5bb6261c016c4bb9f30b56', 'test1@zju.edu.cn')
        insert_data_product(conn, 'demo_for_chart', 150, 200, 170, 70, 120, 230, 400,
                            300, 190, 240, 110, 456.56, '//item.jd.com/100149694564.html', '//img14.360buyimg.com/n7/jfs/t1/258378/14/2438/148797/676a1a18F97c0625d/dc834b70c391a45b.jpg.avif', '京东')
        conn.close()
