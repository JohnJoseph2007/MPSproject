import mysql.connector as msq
from datetime import date

# Connection object, and cursor object.
con = msq.connect(host="localhost", user="root", passwd="jojomeethi2312")
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
        print("\n\n")
        initialise()
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
    print('\n')
    cursor.execute("SELECT * from users")
    userlist = cursor.fetchall()
    for i in userlist:
        if i[1] == x:
            if i[2] == y:
                logged = True
                currentuser = x
                print('Welcome {}!\n\n'.format(i[0].split()[0]))
                main()
            else:
                # Function recall to continue login process until user is logged in.
                print("Wrong password. Try again.")
                login()
    else:
        # Function recall to continue login process until user is logged in.
        print("User not found. Try again.")
        login()

def logout():
    # Logout function.
    global logged
    global currentuser
    confirmation = input("Are you sure you want to log out? (y/n): ")
    if confirmation == 'y':
        print("Logging out.")
        logged = False
        currentuser = None
        # Returns to login function to allow new user to use program
        initialise()
    if currentuser == 'n':
        print("Not logged out yet, returning to main program.")
        # Returns to main function to allow same user to use program
        main()
    
def eventplus():
    # Enter a new entry in the user's table, for a date along with its event.
    y = input("Enter the year: ")
    m = input("Enter the month: ").zfill(2)
    d = input("Enter the day: ").zfill(2)
    ename = "\'{}\'".format(input("What is this event for?: "))
    # Adds leading zeroes (if necessary) into the input day/month/year.
    # For example, 2 -> 02; 24 -> 24; etc.
    # date = "{}-{:2d}-{:2d}".format(y,m,d)
    cursor.execute("INSERT INTO {} (event, day) VALUES ({},\'{}-{}-{}\')".format(currentuser, ename, y,m,d))
    con.commit()
    print("\nSuccessfully added event.\n\n")
    main()

def eventlist():
    # Show all scheduled events for the user
    cursor.execute("SELECT * from {} WHERE day>\'{}\' ORDER BY day".format(currentuser, date.today()))
    events = cursor.fetchall()
    print("All events:\n")
    for i in events:
        print(i[0], "\t-->\t", i[1])
    print("-------\n\n")
    main()

def distance():
    # Finds the number of days until specified date.
    # Uses the `date` constructor from `datetime` package.
    datetofind = input("Enter date to find (YYYY-MM-DD format): ")
    datesplit = datetofind.split("-")
    # date(y,m,d) returns a datetime.date object, which can be used to perform arithmetic operation with other datetime.date objects.
    # Subtracting two datetime.date objects returns another datetime.date object, which contains the difference in time of two dates.
    # date.today() returns the current system date.
    daysuntil = str(date(int(datesplit[0]), int(datesplit[1]), int(datesplit[2]))-date.today()).split(',')[0]
    print("\nDays until specified date: ", daysuntil)
    # Finds all events occurring on that given day.
    cursor.execute("Select * from {}".format(currentuser))
    findevent = cursor.fetchall()
    foundevent = []
    for i in findevent:
        if str(i[1]) == datetofind:
            foundevent.append(i[0])
    print("{} events on that day: {}\n\n".format(len(foundevent), foundevent))
    main()

def dbinit():
    exist = False
    cursor.execute("show databases")
    for i in cursor.fetchall():
        if i[0]=='calendar':
            exist = True
            break
        else: continue
    if not exist:
        cursor.execute("create database calendar")
    cursor.execute("use calendar")
    cursor.execute("show tables")
    if len(cursor.fetchall())==0:
        cursor.execute("create table users(name varchar(30) NOT NULL, userid varchar(64) PRIMARY KEY, userpass varchar(64) UNIQUE NOT NULL)")
        con.commit()

def initialise():
    dbinit()
    # Function to specify new user creation or log in preference.
    print("Good day! Welcome to your calendar. Would you like to `sign up` or `sign in`?")
    sisu = input("\'signup\' to sign up\t\'signin\' to sign in.\n")
    legible = False
    while not legible:
        if sisu == 'signup':
            name = '\'{}\''.format(input("Enter your full name: "))
            username = '\'{}\''.format(input("Username: "))
            password = '\'{}\''.format(input("Password: "))
            createuser(name, username, password)
        elif sisu == 'signin':
            login()
        else:
            print("Input invalid. Please try again.")
    else:
        print('\n\n')

def main():
    while logged:
        # Ask the user what function he/she would like to run
        print("Choose your functionality:")
        print('newe -> Create a new event\nshowe -> Show all events\ntimeb -> Show the time till a date\n')
        print("If you would like to logout, enter \'logout\'\n\n")
        legible = False
        while not legible:
            uinput = input("Your input: ")
            print("\n")
            if uinput == 'newe':
                eventplus()
                legible = True
            elif uinput == 'showe':
                eventlist()
                legible = True
            elif uinput == 'timeb':
                distance()
                legible = True
            elif uinput == 'logout':
                logout()
                legible = True
            else:
                print("User input not valid. Please try again\n")
        else:
            print('\n\n')

if __name__ == "__main__":
    initialise()
