import mysql.connector
from mysql.connector import Error
import getpass

pw = getpass.getpass("Enter password: ")

try:
    connection = mysql.connector.connect(user='root', password=pw,
                              host='127.0.0.1',
                              database='electronics',
                              auth_plugin='mysql_native_password')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")