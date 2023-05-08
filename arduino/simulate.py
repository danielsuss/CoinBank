import serial, time, requests
import random
import sqlite3
import sys

# define random "laser sensor" events

def random_sensor_event():
    # this function will be called every 1-5 seconds
    # it will randomly generate a 60 or 61
    # and return it
    
    # 60 = left sensor
    # 61 = right sensor
    return random.choice([60,61])

def random_time():
    # this function will return a random time between 1 and 5 seconds
    return random.randint(1,5)

# define function to "move the servo"

def move_servo(side="left"):
    multiplier = 1
    if side == "right":
        multiplier = -1
    move_one = 15 * multiplier
    move_two = move_one * -1
    print(f"Servo rotated {move_one} degrees.")
    time.sleep(0.015)
    print("waited 15ms")
    print(f"Servo rotated {move_two} degrees.")
    
# define function to listen for POST requests

def listen_for_requests():
    # this function will listen for POST requests
    # if the POST request is for £1, it will decrement the left counter
    # if the POST request is for £2, it will decrement the right counter
    
    post_request_left = "POST /account/w1 HTTP/1.1"
    post_request_right = "POST /account/w2 HTTP/1.1"
    
    
    

# functions from arduino\python_bidirectional_serial.py

def pass_to_flask(ip, port, flag):
    if flag:
        # left counter incremented
        requests.get(f"http://{ip}:{port}/account/d1") 
    else:
        # right counter incremented
        requests.get(f"http://{ip}:{port}/account/d2")

# get money from existing database

def get_money(username):
    SQL_ALCHEMY_DATABASE_URI = 'sqlite:///..\\database.db'
    con = sqlite3.connect(SQL_ALCHEMY_DATABASE_URI)
    cursor = con.cursor()
    
    cursor.execute(f"SELECT balance FROM users WHERE username = '{username}'")
    money = cursor.fetchone()[0]
    con.close()
    return money
    

# update money in existing database

def update_money(username, money):
    SQL_ALCHEMY_DATABASE_URI = 'sqlite:///..\\database.db'
    con = sqlite3.connect(SQL_ALCHEMY_DATABASE_URI)
    cursor = con.cursor()
    
    cursor.execute(f"UPDATE users SET balance = {money} WHERE username = '{username}'")
    con.commit()
    
    con.close()

username = sys.argv[1]
try:
    money = get_money(username)
except:
    print("User does not exist.")
    exit()
    
try:
    while True:
        time.sleep(random_time())
        laser_event = random_sensor_event()
        
        match laser_event:
            case 60:
                print("Left sensor triggered.")
                money += 1
                pass_to_flask("localhost","5000",True)
            case 61:
                print("Right sensor triggered.")
                money += 2
                pass_to_flask("localhost","5000",False)
            case _:
                print("No sensor triggered.")
        update_money(username, money)
                
except KeyboardInterrupt:
    print("Keyboard interrupt detected. Exiting.")
    
    exit()
    