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
        if user['username'] == userName or user['email'] == email:
            print("username or email already exists")
            return

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    ids = []
    for user in users:
        ids.append(int(user["id"]))
    userId = genId(ids)
    new_user = {"id": userId, "username": userName, "password": hashed_password.decode('utf-8'), "email": email}

    users.append(new_user)

    with open('users.json', 'w') as file:
        json.dump(users, file)
    
    print("User registered successfully")

def genId(ids):
    resId = 0
    for i in ids:
        if i == resId :
            resId+=1
    return resId