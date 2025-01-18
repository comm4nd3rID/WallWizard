
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

def stringReplace(string, s, e, t):
    return string[0:s] + t + string[e:len(string)]

class Quoridor:
    def __init__(self):
        self.board = '''**  **  **  **  **  **  **  **  **
                                  
**  **  **  **  **  **  **  **  **
                                  
**  **  **  **  **  **  **  **  **
                                  
**  **  **  **  **  **  **  **  **
                                  
**  **  **  **  **  **  **  **  **
                                  
**  **  **  **  **  **  **  **  **
                                  
**  **  **  **  **  **  **  **  **
                                  
**  **  **  **  **  **  **  **  **
                                  
**  **  **  **  **  **  **  **  **'''
        self.walls = {'H': [], 'V': []}
        self.players = {'P1': (0, 4), 'P2': (8, 4)}
        self.turn = 'P1'
        self.remaining_walls = {'P1': 10, 'P2': 10}

    def display_board(self):
        p1x,p1y = self.players['P1']
        p2x,p2y = self.players['P2']
        self.board = stringReplace(self.board,(p1y*70) + (p1x*4),(p1y*70) + (p1x*4) + 2,"P1")
        self.board = stringReplace(self.board,(p2y*70) + (p2x*4),(p2y*70) + (p2x*4) + 2,"P2")
        for (i,j) in self.walls['H']:
            self.board = stringReplace(self.board, (70 * j) + 35 + (i * 4), (70 * j) + 35 + (i * 4) + 6,"------")
        for (i,j) in self.walls['V']:
            self.board = stringReplace(self.board, (70 * j) + (i * 4) + 2, (70 * j) + (i * 4) + 2 + 2,"||")
            self.board = stringReplace(self.board, (70 * j) + 70 + (i * 4) + 2, (70 * j) + 70 + (i * 4) + 2 + 2,"||")
            self.board = stringReplace(self.board, (70 * j) + 35 + (i * 4) + 2, (70 * j) + 35 + (i * 4) + 2 + 2,"||")
        print(self.board)
        print(f"P1 walls: {self.remaining_walls['P1']}, P2 walls: {self.remaining_walls['P2']}")

    def play_game(self):
        self.move_pawn('P1', 'down')
        self.place_wall('P1', 'H', (3, 4))
        self.place_wall('P2', 'V', (6, 6))
        self.display_board()

    def play_game(self,turn):
        player = player[turn]
        self.display_board()