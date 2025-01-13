
import json
###import uuid
import bcrypt
import re

def signUp():
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
