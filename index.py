import mysql.connector
print(
    """
========================================================
        Welcome to the Railway Management System
========================================================"""
)

def signup():
    print()
    cursor.execute("SELECT username FROM users")
    users = cursor.fetchall()
    while True:
        username = input("Enter Username (0 To Cancel): ")
        if username == "0":
            return 0
        username = username.lower()
        if (username,) not in users:
            break
        else:
            print("\nUsername Already Exists Try Again!\n")
    password = input("Enter A Password: ")
    name = input("Enter Your Name: ")
    email = input("Enter Your Email: ")
    phoneno = input("Enter Your Phone Number: ")
    address = input("Enter Your Address: ")
    query = 'INSERT INTO users VALUES ("{}","{}","{}","{}","{}","{}",0)'.format(
        username, password, email, name, phoneno, address
    )
    cursor.execute(query)
    connection.commit()
    return username

def login():
    print()
    cursor.execute("SELECT username FROM users")
    users = cursor.fetchall()
    while True:
        username = input("Enter Your Username: ")
        if (username,) in users:
            password = input("Enter Your Password: ")
            cursor.execute(
                "SELECT password FROM users WHERE username = '{}'".format(username)
            )
            if password == cursor.fetchall()[0][0]:
                return username
            else:
                print("\nWrong Password!\n")
        elif username == "0":
            return 0
        else:
            print("\nWrong Username!\n")

def Ticket(id):
    query = """SELECT * 
               FROM tickets
               WHERE ticket_id = {}""".format(
        id
    )
    cursor.execute(query)
    ticket = cursor.fetchone()
    ticket_id = ticket[0]
    train_id = ticket[1]
    username = ticket[2]
    departure_station = ticket[3]
    destination_station = ticket[4]
    price = ticket[5]
    query = """SELECT name,starting_station,ending_station 
               FROM trains 
               WHERE id = {}""".format(
        train_id
    )
    cursor.execute(query)
    train = cursor.fetchone()
    train_name = train[0]
    starting_station = train[1]
    ending_station = train[2]
    query = '''SELECT name 
               FROM users
               WHERE username = "{}"'''.format(
        username
    )
    cursor.execute(query)
    name = cursor.fetchone()[0]
    print(
        """-------------------------------------------------------------------------------
{:^70}
Ticket ID: {}                                       Ticket Price: {} Rupees
		    Name: {}
	    	    Train Starting Station: {}
    		    Train Destination: {}
		    From: {}
		    To: {}
-------------------------------------------------------------------------------""".format(
            train_name,
            ticket_id,
            price,
            name,
            starting_station,
            ending_station,
            departure_station,
            destination_station,
        )
    )
    print()

def TicketMenu():
    while True:
        print(
            """
_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-
            TICKET MENU
        1. View All Tickets
        2. Get Details Of A Specific Ticket
        3. Cancel Ticket
        4. Go Back"""
        )
        choice = input("\n        Enter A Choice >>> ")
        if choice == "1":
            query = """SELECT ticket_id,departure_station,destination_station,name,tickets.train_id 
            FROM tickets,trains 
            WHERE tickets.username = "{}" AND tickets.train_id = trains.id""".format(
                username
            )
            cursor.execute(query)
            tickets = cursor.fetchall()
            if tickets == []:
                print("No Tickets!")
            else:
                print(
                    "\n--------------------------------------------------------------------------------"
                )
                for ticket in tickets:
                    print(
                        "Ticket:({}) | Train:  {} (ID: {}) From {} To {}".format(
                            ticket[0], ticket[3], ticket[4], ticket[1], ticket[2]
                        )
                    )
                    print(
                        "--------------------------------------------------------------------------------"
                    )
        elif choice == "2":
            query = """SELECT ticket_id
                       FROM tickets"""
            cursor.execute(query)
            ids = cursor.fetchall()
            while True:
                id = int(input("Enter The ID Of The Ticket(0 To Go Back): "))
                if id == 0:
                    continue
                elif (id,) in ids:
                    Ticket(id)
                    break
                else:
                    print("\nEnter A Valid ID!\n")
        elif choice == "3":
            cursor.execute("SELECT ticket_id,username FROM tickets")
            ids = cursor.fetchall()
            while True:
                ticket_id = int(
                    input("Enter ID Of The Ticket You Want To Cancel (0 To Go Back): ")
                )
                if ticket_id == 0:
                    break
                elif (ticket_id, username) in ids:
                    query = """SELECT departure_station,destination_station,price,name
                    FROM tickets, trains 
                    WHERE tickets.train_id = trains.id AND tickets.ticket_id = {}""".format(
                        ticket_id
                    )
                    cursor.execute(query)
                    details = cursor.fetchone()
                    if (
                        input(
                            """Are You Sure You Want To Cancel You Ticket On
                {} From {} To {}
Enter Your Choice (Y/N): """.format(
                                details[3], details[0], details[1]
                            )
                        ).upper()
                        == "Y"
                    ):
                        query = "DELETE FROM tickets WHERE ticket_id = {}".format(
                            ticket_id
                        )
                        cursor.execute(query)
                        connection.commit()
                        print("Your Ticket Has Been Cancelled!\n")
                        query = "UPDATE users SET money = money + {} WHERE username = '{}'".format(
                            details[2], username
                        )
                        cursor.execute(query)
                        connection.commit()
                        print("You Have Been Refunded Rupees: {}!".format(details[2]))
                else:
                    print("\nTicket Not Found!\n")
        elif choice == "4":
            break
        else:
            print("\nEnter A Valid Option!\n")

def AdminMenu():
    while True:
        choice = input(
            """\n============ ADMIN MENU ============
        1. View All Trains
        2. View Prices
        3. Add train
        4. Remove Train
        5. Edit Train Details
        6. Add Balance To A User
        7. Logout
        Enter a choice >>> """
        )
        if choice == "1":
            print(
                "\n----------------------------------------------------------------------------------------------------------"
            )
            print("|", end="")
            for i in ("ID", "Name", "Capacity", "Starting Station", "Ending Station"):
                print("{:^20}|".format(i), end="")
            print(
                "\n----------------------------------------------------------------------------------------------------------"
            )
            cursor.execute(
                "SELECT id,name,capacity,starting_station,ending_station FROM trains"
            )
            trains = cursor.fetchall()
            for train in trains:
                print("|", end="")
                for i in train:
                    print("{:^20}|".format(i), end="")
                print(
                    "\n----------------------------------------------------------------------------------------------------------"
                )
            print()
        elif choice == "2":
            print()
            cursor.execute("SELECT id FROM trains")
            ids = cursor.fetchall()
            while True:
                id = int(input("Enter ID Of The Train To View Price (0 To Go Back): "))
                if id == 0:
                    print()
                    break
                elif (id,) in ids:
                    query = "SELECT name,price_1st_class,price_2nd_class,price_3rd_class,price_general FROM trains WHERE id = {}".format(
                        id
                    )
                    cursor.execute(query)
                    train = cursor.fetchone()
                    if train == ():
                        print("\n>>>>> Train Not Found!\n")
                        continue
                    print(
                        """\n            ----------------------------------------
                    Train ID: {}
                    Train Name: {}
                    First Class Price: {}
                    Second Class Price: {}
                    Third Class Price: {}
                    General Price: {}
            ----------------------------------------\n""".format(
                            id, train[0], train[1], train[2], train[3], train[4]
                        )
                    )
                    break
                else:
                    print("\n>>>>> Train Not Found!\n")
                    continue
        elif choice == "3":
            print()
            cursor.execute("SELECT id FROM trains")
            ids = cursor.fetchall()
            while True:
                id = int(input("Enter An ID For The New Train (0 To Go Back): "))
                if id == 0:
                    break
                elif (id,) in ids:
                    print("\n>>>>> Train Already Exists!\n")
                    continue
                else:
                    name = input("Enter A Name For The Train: ")
                    starting_station = input("Enter The Starting Station: ")
                    ending_station = input("Enter The Ending Station: ")
                    capacity = int(input("Enter The Capacity: "))
                    price_1st_class = int(input("Enter The Price For First Class: "))
                    price_2nd_class = int(input("Enter The Price For Second Class: "))
                    price_3rd_class = int(input("Enter The Price For Third Class: "))
                    price_general = int(input("Enter The Price For General: "))
                    query = "INSERT INTO trains VALUES ({},'{}',{},'{}','{}',{},{},{},{})".format(
                        id,
                        name,
                        capacity,
                        starting_station,
                        ending_station,
                        price_1st_class,
                        price_2nd_class,
                        price_3rd_class,
                        price_general,
                    )
                    cursor.execute(query)
                    connection.commit()
                    print("Train Added!\n")
                    break
        elif choice == "4":
            print()
            cursor.execute("SELECT id FROM trains")
            ids = cursor.fetchall()
            while True:
                id = int(input("Enter The ID Of The Train To Remove (0 To Go Back): "))
                if id == 0:
                    break
                elif (id,) in ids:
                    print("Train Removed!\n")
                    query = "DELETE FROM trains WHERE id = {}".format(id)
                    cursor.execute(query)
                    connection.commit()
                    break
                else:
                    print("\n>>>>> Train Not Found!\n")
                    continue
        elif choice == "5":
            print()
            cursor.execute("SELECT id FROM trains")
            ids = cursor.fetchall()
            while True:
                id = int(input("Enter ID Of The Train To Edit (0 To Go Back): "))
                if id == 0:
                    break
                elif (id,) in ids:
                    name = input("Enter New Name Of The Train: ")
                    starting_station = input("Enter The Starting Station: ")
                    ending_station = input("Enter The Ending Station: ")
                    capacity = int(input("Enter The Capacity: "))
                    price_1st_class = int(input("Enter The Price For First Class: "))
                    price_2nd_class = int(input("Enter The Price For Second Class: "))
                    price_3rd_class = int(input("Enter The Price For Third Class: "))
                    price_general = int(input("Enter The Price For General: "))
                    query = """UPDATE trains
                    SET name = '{}',
                    starting_station = '{}',
                    ending_station = '{}',
                    capacity = {},
                    price_1st_class = {},
                    price_2nd_class = {},
                    price_3rd_class = {},
                    price_general = {}
                    WHERE id = {}""".format(
                        name,
                        starting_station,
                        ending_station,
                        capacity,
                        price_1st_class,
                        price_2nd_class,
                        price_3rd_class,
                        price_general,
                        id,
                    )
                    cursor.execute(query)
                    connection.commit()
                    print("Train Edited!\n")
                    break
                else:
                    print("\n>>>>> Train Not Found!\n")
                    continue
        elif choice == "6":
            print()
            cursor.execute("SELECT username FROM users")
            usernames = cursor.fetchall()
            while True:
                username = input("Enter Username Of User (0 To Go Back): ")
                if username == "0":
                    print()
                    break
                elif (username,) in usernames:
                    balance = int(input("How Much Money Do You Want To Add: "))
                    query = "UPDATE users SET money = money + {} WHERE username = '{}'".format(
                        balance, username
                    )
                    cursor.execute(query)
                    connection.commit()
                    break
                else:
                    print("\n>>>>> Username Not Found!\n")
        elif choice == "7":
            print("\nYou have been logged out!\n")
            break
        else:
            print("\n>>>>> Enter a valid option!\n")

def UserMenu(username):
    while True:
        choice = input(
            """\n============ MENU ============
        1. View Trains
        2. Buy Ticket
        3. View Tickets
        4. View User Details
        5. Edit User Details
        6. Deposit Money
        7. Change Password
        8. Logout
        Enter a choice >>> """
        )
        if choice == "1":
            print(
                "\n----------------------------------------------------------------------------------------------------------"
            )
            print("|", end="")
            for i in ("ID", "Name", "Capacity", "Starting Station", "Ending Station"):
                print("{:^20}|".format(i), end="")
            print(
                "\n----------------------------------------------------------------------------------------------------------"
            )
            cursor.execute(
                "SELECT id,name,capacity,starting_station,ending_station FROM trains"
            )
            trains = cursor.fetchall()
            for train in trains:
                print("|", end="")
                for i in train:
                    print("{:^20}|".format(i), end="")
                print(
                    "\n----------------------------------------------------------------------------------------------------------"
                )
            print()
        elif choice == "2":
            cursor.execute("SELECT MAX(ticket_id) FROM tickets")
            ticket_id = cursor.fetchone()[0] + 1
            cursor.execute("SELECT id FROM trains")
            ids = cursor.fetchall()
            while True:
                train_id = int(input("Enter Train ID: "))
                if (train_id,) in ids:
                    departure_station = input("Enter Station Of Departure: ")
                    destination_station = input("Enter Destination: ")
                    while True:
                        choice = input(
                            """                    Select Class
                        1. 1st Class
                        2. 2nd Class
                        3. 3rd Class
                        4. General
    Enter Your Choice >>> """
                        )
                        if choice == "1":
                            Class = "price_1st_class"
                            break
                        elif choice == "2":
                            Class = "price_2nd_class"
                            break
                        elif choice == "3":
                            Class = "price_3rd_class"
                            break
                        elif choice == "4":
                            Class = "price_general"
                            break
                        else:
                            print("\nEnter A Valid Option!\n")
                    query = "SELECT {} FROM trains WHERE id = {}".format(
                        Class, train_id
                    )
                    cursor.execute(query)
                    price = cursor.fetchone()[0]
                    cursor.execute(
                        'SELECT money FROM users WHERE username = "{}"'.format(username)
                    )
                    balance = cursor.fetchone()[0]
                    if balance < price:
                        print("\nNot Enough Money In Your Account!\n")
                        break
                    query = (
                        'INSERT INTO tickets VALUES ({},{},"{}","{}","{}",{})'.format(
                            ticket_id,
                            train_id,
                            username,
                            departure_station,
                            destination_station,
                            price,
                        )
                    )
                    cursor.execute(query)
                    newbalance = balance - price
                    cursor.execute(
                        'UPDATE users SET money = {} WHERE username = "{}"'.format(
                            newbalance, username
                        )
                    )
                    connection.commit()
                    print("Ticket Purchased!")
                    break
                else:
                    print("\nEnter A Valid Train ID!\nPress 1 To View Trains.\n")
                    break
        elif choice == "3":
            TicketMenu()
        elif choice == "4":
            query = 'SELECT email,name,phoneno,address,money FROM users WHERE username = "{}"'.format(
                username
            )
            cursor.execute(query)
            details = cursor.fetchone()
            print(
                """
            Name: {}
            Username: {}
            Email: {}
            Phone No: {}
            Address: {}
            Balance: {}\n""".format(
                    details[1], username, details[0], details[2], details[3], details[4]
                )
            )
        elif choice == "5":
            print("\nEnter New Details")
            email = input("Enter A Email: ")
            name = input("Enter Name: ")
            phoneno = input("Enter Phone No: ")
            address = input("Enter Address: ")
            query = """UPDATE users SET 
                       email = '{}',
                       name = '{}',
                       phoneno = '{}',
                       address = '{}'
                       WHERE username = '{}'""".format(
                email, name, phoneno, address, username
            )
            cursor.execute(query)
            connection.commit()
            print("Details Edited!\n")
        elif choice == "6":
            balance = int(input("\nHow Much Money Do You Want To Add: "))
            query = "UPDATE users SET money = money + {} WHERE username = '{}'".format(
                balance, username
            )
            cursor.execute(query)
            connection.commit()
            print("Money Deposited!\n")
        elif choice == "7":
            newpassword = input("\nEnter New Password: ")
            query = "UPDATE users SET password = '{}' WHERE username = '{}'".format(
                newpassword, username
            )
            cursor.execute(query)
            connection.commit()
            print("Password Changed!\n")
        elif choice == "8":
            print("\nYou have been logged out!\n")
            break
        else:
            print("\nEnter A Valid Option!\n")

def sql():
    cursor.execute("CREATE DATABASE IF NOT EXISTS railway")
    cursor.execute("USE railway")
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users (
                      username VARCHAR(100) PRIMARY KEY,
                      PASSWORD VARCHAR(100),
                      email VARCHAR(255),
                      NAME VARCHAR(255),
                      phoneno VARCHAR(15),
                      address VARCHAR(255),
                      money INT
                      )"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS tickets (
                      ticket_id INT PRIMARY KEY,
                      train_id INT,
                      username VARCHAR(255),
                      departure_station VARCHAR(255),
                      destination_station VARCHAR(255),
                      price INT
                      )"""
    )
    cursor.execute("SELECT ticket_id FROM tickets")
    if (0,) not in cursor.fetchall():
        cursor.execute('INSERT INTO tickets VALUES (0,0,"0","0","0",0)')
    connection.commit()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS trains (
                      id INT PRIMARY KEY,
                      name VARCHAR(255),
                      capacity INT,
                      starting_station VARCHAR(255),
                      ending_station VARCHAR(255),
                      price_1st_class INT,
                      price_2nd_class INT,
                      price_3rd_class INT,
                      price_general INT
                    )"""
    )
    cursor.execute("SELECT username FROM users")
    if ("admin",) not in cursor.fetchall():
        cursor.execute(
            'INSERT INTO users VALUES ("admin","admin@123","admin@gmail.com","Administrator","+91 1234567890","SAPS, Anakkal",10000)'
        )
    connection.commit()
username = input("Enter username for the sql connection: ")
pword = input("Enter password for the sql connection: ")
try:
    connection = mysql.connector.connect(
        host="localhost", user=username, password="pixelplayz"
    )
    if connection.is_connected():
        cursor = connection.cursor()
        sql()
        while True:
            choice = input(
                """\n
===============  Menu ===============
            1. Login
            2. Signup
            3. Exit
            
            Enter your choice >>> """
            )
            if choice == "1":
                username = login()
                if username == "admin":
                    AdminMenu()
                elif username == 0:
                    continue
                else:
                    UserMenu(username)
            elif choice == "2":
                username = signup()
                if username == 0:
                    continue
                elif username == "admin":
                    AdminMenu()
                else:
                    UserMenu(username)
            elif choice == "3":
                break
            else:
                print("\n>>>>> Enter a valid option!\n")
        connection.close()
except Exception as e:
    print(e)
    print("Couldn't Connect To Database")
