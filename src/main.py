import mysql.connector as msq

con = msq.connect(host="localhost", user="root", passwd="jojomeethi2312", database="calendar")
cursor = con.cursor()

def createuser(name, username, password):
    # Creates a user profile based on given name and password.
    try:
        # Inserting user values into table
        cursor.execute("INSERT INTO users (name, userid, userpass) VALUES ({},{},{})".format(name, username, password))
        # Creating a table for each user.
        cursor.execute("CREATE TABLE {} (event varchar(50) PRIMARY KEY, day date NOT NULL)".format(username[1:-1]))
        con.commit()
    except Exception as e:
        print("Error occurred.")
        print(e)

def login():
    pass
    
def eventplus(d, m, y, ename, ulogin):
    date = "{:4d}-{:2d}-{:2d}".format(y,m,d)
    cursor.execute("INSERT INTO {} (event, day) VALUES ({},{})".format(ulogin, ename, date))
    con.commit()

def distance():
    pass

def reset():
    cursor.execute("DELETE from users")
    con.commit()

def main():
    # createuser('\"John Joseph\"', '\"johnjoseph357\"', '\"jj124\"')
    reset()


main()