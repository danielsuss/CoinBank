import keyboard
import requests

while True:
    keyboard.wait('q')
    print('£1 deposited')
    requests.get("http://localhost:5000/account/d1")
    