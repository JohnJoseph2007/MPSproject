import mysql.connector as msq
from datetime import date

# Connection object, and cursor object.
con = msq.connect(host="localhost", user="root", passwd="jojomeethi2312", database="calendar")
cursor = con.cursor()

# Keeping in check whether a user is/isn't logged in.
logged = False
ulogin = ""

def createuser(name, username, password):
    # Creates a user profile based on given name and password.
    try:
        # Inserting user values into table.
        cursor.execute("INSERT INTO users (name, userid, userpass) VALUES ({},{},{})".format(name, username, password))
        # Creating a table for each user.
        cursor.execute("CREATE TABLE {} (event varchar(50) PRIMARY KEY, day date NOT NULL)".format(username[1:-1]))
        con.commit()
    except Exception as e:
        print("Error occurred.")
        print(e)

def login():
    # Login function.
    print("You are not currently logged in. Log in:")
    x = input("Username: ")
    y = input("Password: ")
    cursor.execute("SELECT * from users")
    userlist = cursor.fetchall()
    for i in userlist:
        if i[1] == x:
            if i[2] == y:
                logged = True
                ulogin = x
            else:
                print("Wrong password. Try again.")
                login()
    else:
        print("User not found. Try again.")
        login()
    
def eventplus():
    # Enter a new entry in the user's table, for a date along with its event.
    y = int(input("Enter the year: "))
    m = int(input("Enter the month: "))
    d = int(input("Enter the day: "))
    ename = input("What is this event for?: ")
    date = "{:4d}-{:2d}-{:2d}".format(y,m,d)
    cursor.execute("INSERT INTO {} (event, day) VALUES ({},{})".format(ulogin, ename, date))
    con.commit()

def distance():
    # Finds the number of days until specified date.
    # Uses the `date` constructor from `datetime` package.
    datetofind = input("Enter date to find (YYYY-MM-DD format): ").split("-")
    # date.today() returns the current date
    datenow = date.today()
    datetill = date(datetofind[0], datetofind[1], datetofind[2])
    daysuntil = datetill - datenow
    print("Days until specified date: ", daysuntil.days)


def reset():
    # Reset the entire database, to its original state.
    cursor.execute("DELETE from users")
    cursor.execute("SHOW tables")
    tablelist = cursor.fetchall()
    for i in tablelist:
        cursor.execute("DROP table {}".format(i))
    con.commit()

while logged:
    pass

# WHAT'S LEFT:
#  Make a main module-ish
#  Test code
#  Publish!