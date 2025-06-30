
import mysql.connector as mycon
mydb=mycon.connect(host="localhost",user="root",passwd="Pawasthi@8127",database="nitj")
mycursor=mydb.cursor()
sql="select * from  fe2  WHERE `Roll No.`=24106050"
mycursor.execute(sql)
myrecord = mycursor.fetchone()
print("The Data fetched from official website of NIT J regarding the student is:" '''C:(www.nitj.ac.in) ''')
print(myrecord)


