import mysql.connector

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ShadowSlash247",
        database="mydatabase"
        )

mycursor = mydb.cursor()
# val = (url,created_at,username)
sql = "SELECT url, COUNT(url) FROM tweettest GROUP BY url"
# mycursor.execute("SELECT ame FROM workers WHERE symbol=%s", (name,))
# val = (url, created_at
mycursor.execute(sql)
# print(mycursor.statement)
# print(mycurs

data = mycursor.fetchall()

print(data[0][0])

for i in data:
    # print(i[0])
    sql = "INSERT INTO urltest (url, frequency) VALUES (%s,%s)"
    val = ([i[0], i[1]])
    mycursor.execute(sql,val)
mydb.commit()

# if len(data) == 0:
#     return True
# else:
#     return False