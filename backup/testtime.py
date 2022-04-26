# import mysql.connector

# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="",
#     database="counting_ststem"
# )
# mycursor = mydb.cursor()

# mycursor.execute("SHOW DATABASES")

# for x in mycursor:
#     print(x)


# import counting_people
# import mysql.connector
# from mysql.connector import Error
# from mysql.connector import errorcode

# try:
#     connection = mysql.connector.connect(host='localhost',
#                                          database='counting_ststem',
#                                          user='root',
#                                          password='')
#     mySql_insert_query = """INSERT INTO counting_ststem.count_proc (count_id ,fac_id, start_time,end_time,data_stamp,current_person,time_per_person)
#                            VALUES
#                            (null ,1 ,'2021-02-20 14:34:35','2021-02-20 14:34:35','2021-02-20 14:34:35',2,2.6); """

#     cursor = connection.cursor()
#     cursor.execute(mySql_insert_query)
#     connection.commit()
#     print(cursor.rowcount, "Record inserted successfully into Laptop table")
#     cursor.close()ไ

# except mysql.connector.Error as error:
#     print("Failed to insert record into Laptop table {}".format(error))

# finally:
#     if (connection.is_connected()):
#         connection.close()
#         print("MySQL connection is closed")

import mysql.connector
import psycopg2
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="",
#     database="counting_ststem"
# )

mydb = psycopg2.connect(database="d7gs7158vj1qqf"
    , user="tdlprgyfdfqyaz"
    , password="5fd1a43acec22dcfe5f1cbef4c338e4dda65d29f3fdcb378244969f85dc644ce"
    , host="ec2-3-218-171-44.compute-1.amazonaws.com"
    , port="5432")
mycursor = mydb.cursor()

# mycursor = mydb.cursor()

mycursor.execute("select num_of_graduates , fac_name from faculty f ")

myresult = mycursor.fetchall()

num_of_graduates = []
fac_name = []

for faculty in myresult:
    print(faculty)
    num_of_graduates.append(faculty[0])
    fac_name.append(faculty[1])

# print(num_of_graduates[:,''])

# print(num_of_graduates[1],fac_name[1])


# print('Enter Strat Time :')
# start = input()
# print('Enter End Time :')
# start = input()
# print('Enter Amount of Student :')
# amountStudent = input()
