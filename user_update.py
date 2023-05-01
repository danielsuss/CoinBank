def get_user():
    with open('user.txt', 'r') as f:
        user = f.readline()
        f.close()
        return user
    
    
def update_user(user):
    with open('user.txt', 'w') as f:
        f.write(user)
        f.close()