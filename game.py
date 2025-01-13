
import json
###import uuid
import bcrypt
import re

def signUp():
    global userName
    userName = input("Enter username: ")
    password = input("Enter password (more than 8 characters): ")
    email = input("Enter email: ")

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Invalid email format")
        return
   
    with open('users.json', 'r') as file:
        users = json.load(file)

    for user in users:
        if users[user]['username'] == userName or users[user]['email'] == email:
            print("username or email already exists")
            return

    hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    ids = []
    for user in users:
        ids.append(int(users[user]["id"]))
    userId = genId(ids)
    newUser = {"id": userId, "username": userName, "password": hashedPassword.decode('utf-8'), "email": email}

    users[userId] = newUser

    with open('users.json', 'w') as file:
        json.dump(users, file)
    
    print("User registered successfully")

def genId(ids):
    resId = 0
    for i in ids:
        if i == resId :
            resId+=1
    return resId

def login():
    userName = input("Enter username: ")
    password = input("Enter password: ")

    with open('users.json', 'r') as file:
        users = json.load(file)
    
    for user in users:
        if users[user]['username'] == userName and bcrypt.checkpw(password.encode('utf-8'), users[user]['password'].encode('utf-8')):
            print("Login successful")
            return user

    print("Invalid username or password")
    return None

print("    corridor    ")
print("    Sign Up : 1 ")
print("    Login : 2")
def menu_1():
    inp = input("enter the code:")
    if inp == "1":
        signUp()
        menu_1()
    elif inp =="2":
        login()
    else :  
        print("enter valid number")
        menu_1()
    return None
def menu_2():
    print(f"you loged in succesfully! {userName}")
    print("    New game: 1")
    print("    Load game: 2")
    print("    Best players: 3")
    inp_2 = input("enter the code:")
    if inp_2 == "1":
        None
        # start game
    elif inp_2 == "2":
        None
        # Load previous games
    elif inp_2 == "3":
        None
        # show the list of best players
    else :
        menu_2()
    return None
