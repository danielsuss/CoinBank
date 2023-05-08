import serial, time, requests

def pass_to_flask(ip, port, flag):
    if flag:
        # left counter incremented
        requests.get(f"http://{ip}:{port}/account/d1") 
    else:
        # right counter incremented
        requests.get(f"http://{ip}:{port}/account/d2")

# get counters from existing data
# if there are no counters, set them to 0
def get_counters():
    try:
        with open('counters.txt', 'r') as f:
            left_counter = int(f.readline())
            right_counter = int(f.readline())
    except:
        left_counter = 0
        right_counter = 0
    return left_counter, right_counter

def set_counters(left_counter, right_counter):
    with open('counters.txt', 'w') as f:
        f.write(str(left_counter) + '\n')
        f.write(str(right_counter) + '\n')


if __name__ == '__main__':
    ser = serial.Serial('COM5', 9600, timeout=1)
    ser.reset_input_buffer()
    
    left_counter, right_counter = get_counters()
    
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
