import socket
import threading
import time
# 001 = name
# 002 = password
# 003 = access got
# 004 = access don't got

# 005 = new account
# 005.1 = new account name is already in list(names) on the server
# 006 = Login

# 007 = Napisz wiadomość
# 007.1 = imię nie wystepuje
# 007.2 = imię występuje
# 008 = Odczytaj wiadomość

# 009 = Wyloguj się

HOST = 'public ipv4 host or local if you on same device'
PORT = 5050
transmision_type = 'utf8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect((HOST,PORT))
    print(f'Connecting with server at {HOST}:{PORT}.')
except:
    print(f'Connection with sever it is impossible\nCheck your network and PING\nYour current version is 1.0, maby the server has been changed to a newer version.')



class User:
    def __init__(self, Login):
        self.Login = Login
        self.current_name = None
        self.menu_decision = None



    def login(user):
        if user.menu_decision == 'LI' and user.Login == False:
            choice = '006'
            client.send(choice.encode(transmision_type))
            while user.Login == False:
                name = str(input('Username: '))
                password = str(input('Password: '))
                client.send(name.encode(transmision_type))
                client.send(password.encode(transmision_type))
    
                feedback = client.recv(1024).decode(transmision_type)

                if feedback == '003':
                    user.Login = True
                    print('Access granted')
                    user.current_name = name
                    break
                if feedback == '004':
                    user.Login = False
                    print('Access denied')


    def create_account(user):
        if user.menu_decision == 'CA' and user.Login == True:
            print('If you want create new account you must Logout.')
        if user.menu_decision == 'CA' and user.Login == False:
            choice = '005'
            client.send(choice.encode(transmision_type))
            name = str(input('New username: '))
            password = str(input('New password: '))
            password_2 = str(input('Please enter your password again: '))
            while password != password_2:
                print('The passwords do not match')
                password = str(input('New password: '))
                password_2 = str(input('Please enter your password again: '))
                if password == password_2:
                    break
            else:
                client.send(name.encode(transmision_type))
                client.send(password.encode(transmision_type))
            name_req = client.recv(1024).decode(transmision_type)
            while name_req == '005.1':
                name = str(input('Your username is already use please enter New username: '))
                client.send(name.encode(transmision_type))
                name_req = client.recv(1024).decode(transmision_type)
                if name_req == '005.2':
                    user.Login = True
                    user.current_name = name
                    print('Successfully created account.')
                    break
            else:
                print('Successfully created account.')
                user.Login = True
                user.current_name = name


    def reading_mail(user):
        if user.menu_decision == 'RM' and user.Login == True:
            choice = '008'
            client.send(choice.encode(transmision_type))
            
            list_of_messages = client.recv(1024).decode(transmision_type)
            print(list_of_messages)

    def writing_mail(user):
        if user.menu_decision == 'WM' and user.Login == True:
            choice = '007'
            client.send(choice.encode(transmision_type))
            
            o = str(input("Recipient's name: "))
            print(f'Sender: {user.current_name} ')
            c = user.current_name
            p = str(input('Write one-line message: '))

            client.send(o.encode(transmision_type))
            time.sleep(0.3)
            client.send(c.encode(transmision_type))
            time.sleep(0.3)
            client.send(p.encode(transmision_type))
            
            name_occurs = client.recv(1024).decode(transmision_type)
            while name_occurs == '007.1':
                print("This Recipient's name no occurs")
                o = str(input("Recipient's name: "))
                print(f'Sender: {user.current_name} ')
                c = user.current_name
                p = str(input('Write one-line message: '))
                client.send(o.encode(transmision_type))
                time.sleep(0.3)
                client.send(c.encode(transmision_type))
                time.sleep(0.3)
                client.send(p.encode(transmision_type))

                name_occurs = client.recv(1024).decode(transmision_type)
                
                if name_occurs == '007.2':
                    print('Created e-mail successfully.')
                    break
            client.send(o.encode(transmision_type))
            time.sleep(0.3)
            client.send(c.encode(transmision_type))
            time.sleep(0.3)
            client.send(p.encode(transmision_type))
            print('Created e-mail successfully.')


    def logout(user):
        if user.menu_decision == 'LO' and user.Login == True:
            choice = '009'
            client.send(choice.encode(transmision_type))
            user.Login = False
            user.current_name = None
            print('Sucessfuly logout')


    def menu():
        user = User(False)
        user.menu_decision = None
        while True and user.Login == False:
            time.sleep(1)
            user.menu_decision = input(str('======Menu======\nLog in => "LI"\nCreate account => "CA"\nTo exit => "exit"\n======Menu======: '))
            user.exit()
            user.login()
            user.create_account()
        
        while True and user.Login == True:
            time.sleep(1)
            user.menu_decision = input(str('======Menu======\nWrite an e-mail => "WM"\nRead the e-mail => "RM"\nLogout => "LO"\nTo exit => "exit"\n======Menu======: '))
            user.exit()
            user.writing_mail()
            user.reading_mail()
            user.logout()


    def exit(user):
        if user.menu_decision == 'exit':
            choice = '010'
            client.send(choice.encode(transmision_type))
            client.close()
            user.Login = False
            user.current_name = None
            user.menu_decision = None
            time.sleep(0.5)
            exit()



user = User

while True:
    user.menu()