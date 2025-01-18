import json
###import uuid
import bcrypt
import re
users = {}
userId = 0
checked = []
def wall_check(p,wall,n):
    if p in checked:
        return False
    checked.append(p)
    if p[1] == n:
        return True
    if (p[0],p[1]+1) not in wall['V'] and (p[0],p[1]) not in wall['V'] and p[0] < 8:
        if wall_check((p[0]+1,p[1]),wall,8):
            return True
    if (p[0]-1,p[1]-1) not in wall['V'] and (p[0]-1,p[1]) not in wall['V'] and p[0] > 0:
        if wall_check((p[0]-1,p[1]),wall,8):
            return True
    if (p[0],p[1]) not in wall['H'] and (p[0]-1,p[1]) not in wall['H'] and p[1] > 0:
        if wall_check((p[0],p[1]-1),wall,8):
            return True
    if (p[0],p[1]-1) not in wall['H'] and (p[0]-1,p[1]-1) not in wall['H'] and p[1] < 8:
        if wall_check((p[0],p[1]+1),wall,8):
            return True
    return False        
       
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
        global users
        users = json.load(file)
    
    for user in users:
        if users[user]['username'] == userName and bcrypt.checkpw(password.encode('utf-8'), users[user]['password'].encode('utf-8')):
            print("Login successful")
            
            return user

    print("Invalid username or password")
    return False

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
        cboard = self.board
        cboard = stringReplace(cboard,(p1y*70) + (p1x*4),(p1y*70) + (p1x*4) + 2,"P1")
        cboard = stringReplace(cboard,(p2y*70) + (p2x*4),(p2y*70) + (p2x*4) + 2,"P2")
        for (i,j) in self.walls['H']:
            cboard = stringReplace(cboard, (70 * j) + 35 + (i * 4), (70 * j) + 35 + (i * 4) + 6,"------")
        for (i,j) in self.walls['V']:
            cboard = stringReplace(cboard, (70 * j) + (i * 4) + 2, (70 * j) + (i * 4) + 2 + 2,"||")
            cboard = stringReplace(cboard, (70 * j) + 70 + (i * 4) + 2, (70 * j) + 70 + (i * 4) + 2 + 2,"||")
            cboard = stringReplace(cboard, (70 * j) + 35 + (i * 4) + 2, (70 * j) + 35 + (i * 4) + 2 + 2,"||")
        print(cboard)
        print(f"P1 walls: {self.remaining_walls['P1']}, P2 walls: {self.remaining_walls['P2']}")

    def move_pawn(self, player, direction):
        x, y = self.players[player]
        if direction == 'left' and x > 0:
            self.players[player] = (x-1, y)
        elif direction == 'right' and x < 8:
            self.players[player] = (x+1, y)
        elif direction == 'down' and y > 0:
            self.players[player] = (x, y+1)
        elif direction == 'up' and y < 8:
            self.players[player] = (x, y-1)
        else:
            print("Invalid move")
            self.move_pawn(player,input("Enter direction (up, down, left, right): "))
        x, y = self.players[player]

    def place_wall(self, player):
        position = (0,0)
        orientation = input("Enter orientation (horizontal ,vertical) :")
        if(orientation != "horizontal" and orientation != "vertical"):
            print("Invalid orientation")
            self.place_wall(player)
            return
        
        i = input("Enter i (1 to 8):")
        if(not int(i)):
            print("Invalid i")
            self.place_wall(player)
            return
        
        j = input("Enter j (1 to 8):")
        if(not int(j)):
            print("Invalid j")
            self.place_wall(player)
            return
        
        position = (int(i), int(j))
        
        if self.remaining_walls[player] > 0:
            walls = self.walls
            walls['H' if orientation=="horizontal" else 'V'].append(position)
            if not (wall_check(self.players['P1'],walls,8) and wall_check(self.players['P2'],walls,0)):
               print("Cant put that there")
               self.place_wall(player)
               return
            self.walls[orientation].append(position)
            self.remaining_walls[player] -= 1
            
            
    def play_game(self,turn):
        print(users[self.p1ID]['username'] + " as P1 VS " + users[self.p2ID]['username'] + " as P2!")
        print(turn + "s Turn")
        (i1, j1) = self.players['P1']
        (i2, j2) = self.players['P2']
        if(j1 == 8):
                print(users[self.p1ID]['username'] + "Won!")
                return self
        else:
            if(j2 == 0):
                print(users[self.p2ID]['username'] + " Won!")
                return self
        
        self.display_board()
        inp = input("Choose an option (placewall, moveplayer): ")
        if(inp != "placewall" and inp != "moveplayer"):
            self.play_game(turn)
            return
        elif(inp == "moveplayer"):
            self.move_pawn(turn,input("Enter direction (up, down, left, right): "))
        else:
            if not (self.remaining_walls[turn] > 0):
                print(f"No remaining walls for {turn}")
                self.play_game(turn)
                return
            else:
                self.place_wall(turn)
        self.play_game("P1" if(turn == "P2") else "P2")


def menu_2():

    print("    New game: 1")
    print("    Load game: 2")
    print("    Best players: 3")
    inp_2 = input("enter the code:")
    if inp_2 == "1":
        l = login()
        if(not l):
            menu_2()
            return
        else:
            game = Quoridor(userId,l)
            game.play_game('P1')
        # start game
    elif inp_2 == "2":
        None
        # Load previous games
    elif inp_2 == "3":
        None
        # show the list of best players
    else :
        menu_2()
        return
    return None

def menu_1():
    print("    corridor    ")
    print("    Sign Up : 1 ")
    print("    Login : 2")
    inp = input("enter the code:")
    if inp == "1":
        signUp()
        menu_1()
        return
    elif inp =="2":
        user_id = login()
        if(user_id == False):
            menu_1()
            return
        else :
            global userId
            userId = user_id
            print(f"you loged in succesfully! {users[userId]['username']}")
            menu_2()
            return
    else :  
        print("enter valid number")
        menu_1()
        return

menu_1()