import mysql.connector as msq
from datetime import date

# Connection object, and cursor object.
con = msq.connect(host="localhost", user="root", passwd="jojomeethi2312", database="calendar")
cursor = con.cursor()

# Keeping in check whether a user is/isn't logged in.
logged = False
currentuser = None

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
    global logged
    global currentuser
    print("You are not currently logged in. Log in:")
    x = input("Username: ")
    y = input("Password: ")
    cursor.execute("SELECT * from users")
    userlist = cursor.fetchall()
    for i in userlist:
        if i[1] == x:
            if i[2] == y:
                logged = True
                currentuser = x
            else:
                # Function recall to continue login process until user is logged in.
                print("Wrong password. Try again.")
                login()
    else:
        # Function recall to continue login process until user is logged in.
        print("User not found. Try again.")
        login()

def logout():
    global logged
    global currentuser
    # Logout function
    confirmation = input("Are you sure you want to log out? (y/n): ")
    if confirmation == 'y':
        print("Logging out.")
        logged = False
        currentuser = None
        # Returns to login function to allow new user to use program
        login()
    if currentuser == 'n':
        print("Not logged out yet, returning to main program.")
        # Returns to main function to allow same user to use program
        main()
    
def eventplus():
    # Enter a new entry in the user's table, for a date along with its event.
    y = int(input("Enter the year: "))
    m = int(input("Enter the month: "))
    d = int(input("Enter the day: "))
    ename = input("What is this event for?: ")
    # Adds leading zeroes (if necessary) into the input day/month/year.
    # For example, 2 -> 02; 24 -> 24; etc.
    date = "{:4d}-{:2d}-{:2d}".format(y,m,d)
    cursor.execute("INSERT INTO {} (event, day) VALUES ({},{})".format(currentuser, ename, date))
    con.commit()
    print("Successfully added event.\n\n")

def eventlist():
    # Show all scheduled events for the user
    cursor.execute("SELECT from {} * WHERE day>{}-{}-{}".format(currentuser, date.year, date.month, date.day))
    events = cursor.fetchall()
    print("All events:\n")
    for i in events:
        print(i[0], "\t-->\t", i[1])
    print("x--x--x\n\n")

def distance():
    # Finds the number of days until specified date.
    # Uses the `date` constructor from `datetime` package.
    datetofind = input("Enter date to find (YYYY-MM-DD format): ")
    datesplit = datetofind.split("-")
    # date.today() returns the current date
    datenow = date.today()
    datetill = date(datesplit[0], datesplit[1], datesplit[2])
    # Subtracting two date objects returns another date object containing the amount of time between them
    daysuntil = datetill - datenow
    print("Days until specified date: ", daysuntil.days)
    # Finds all events occurring on that given day.
    cursor.execute("Select * from {}".format(currentuser))
    findevent = cursor.fetchall()
    foundevent = []
    for i in findevent:
        if str(i[1]) == datetofind:
            foundevent.append(i[0])
    print("{} events on that day: {}".format(len(foundevent), foundevent))


def reset():
    # Reset the entire database, to its original state.
    cursor.execute("DELETE from users")
    cursor.execute("SHOW tables")
    tablelist = cursor.fetchall()
    for i in tablelist:
        cursor.execute("DROP table {}".format(i))
    con.commit()

def initialise():
    # Function to specify new user creation or log in preference.
    print("Good day! Welcome to your calendar. Would you like to `sign up` or `sign in`?")
    sisu = input("\'signup\' to sign up\t\'signin\' to sign in.")
    legible = False
    while not legible:
        if sisu == 'signup':
            createuser()

def main():
    while logged:
        # Ask the user what function he would like to run
        print('Welcome {}!'.format(currentuser))
        print("Choose your functionality:")
        print('newe -> Create a new event\nshowe -> Show all events\ntimeb -> Show the time till a date\n\n')
        print("If you would like to logout, enter \'logout\'")
        legible = False
        while not legible:
            uinput = input("Your input: ")
            if uinput == 'newe':
                eventplus()
                print('\n')
                legible = True
            elif uinput == 'showe':
                eventlist()
                print('\n')
                legible = True
            elif uinput == 'timeb':
                distance()
                print('\n')
                legible = True
            elif uinput == 'logout':
                logout()
                legible = True
            else:
                print("User input not valid. Please try again\n")
    

# WHAT'S LEFT:
#  Make a main module-ish
#  Test code
#  Publish!
