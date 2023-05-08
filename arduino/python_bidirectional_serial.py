import serial, time, requests
import sqlite3, sys

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

if __name__ == '__main__':
    ser = serial.Serial('COM5', 9600, timeout=1)
    ser.reset_input_buffer()
    
    username = sys.argv[1]
    try:
        money = get_money(username)
    except:
        print("User does not exist.")
        exit()
    
    left_counter = 0
    right_counter = 0
    
    while True:
        number = ser.read()
        if number != b'':
            if int.from_bytes(number, byteorder='big') == 60:
                print('Left sensor triggered.')
                left_counter += 1
                pass_to_flask("127.0.0.1",5000,True)
            elif int.from_bytes(number, byteorder='big') == 61:
                print('Right sensor triggered.')
                right_counter += 1
                pass_to_flask("127.0.0.1",5000,False)

# To do: communicate this to flask app
