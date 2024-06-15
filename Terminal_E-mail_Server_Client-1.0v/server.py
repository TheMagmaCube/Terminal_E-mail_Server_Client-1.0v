import socket
import threading
import time
# Odbiorca == o
# Adresat == c
# Wiadomość == p

# 001 = name
# 002 = password
# 003 = access got
# 004 = access don't got

# 005 = new account
# 005.1 = new account name is already on the list(names) chose other
# 006 = Login

# 007 = Napisz wiadomość
# 007.1 = imię nie występuje
# 008 = Odczytaj wiadomość

# 009 = Wyloguj się
print('Server: Starting...')

HOST = 'local ipv4 host'
PORT = 5050
transmision_type = 'utf8'

print(f'Server listening at {HOST}:{PORT}.')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()



class Client:
    def __init__(self,Login):
        self.Login = Login
        self.current_name = None
        self.menu_decision = None
        self.messages = []
        self.names = []
        self.passwords = []
        self.Exit = False

    def login(self):        
        if client_log.menu_decision == '006' and client_log.Login == False:
            while client_log.Login == False:
                name_user = client.recv(1024).decode(transmision_type)
                password_user = client.recv(1024).decode(transmision_type)
                if name_user in client_log.names and password_user in client_log.passwords:
                    i = client_log.names.index(name_user)
                    if name_user == client_log.names[i] and password_user == client_log.passwords[i]:
                        client.send('003'.encode(transmision_type))
                        client_log.Login = True
                        client_log.current_name = name_user
                        print(f'Server: {address[0]}:{address[1]} successfully login on {name_user}.')
                    else:
                        client.send('004'.encode(transmision_type))
                        print(f'Server: {address[0]}:{address[1]} tried to login, but unsuccessfully')
                else:
                    client.send('004'.encode(transmision_type))
                    print(f'Server: {address[0]}:{address[1]} tried to login, but unsuccessfully')
        
            
    

    def create_account(self):        
        if client_log.menu_decision == '005' and client_log.Login == False:
            new_name = client.recv(1024).decode(transmision_type)
            new_password = client.recv(1024).decode(transmision_type)
            while new_name in client_log.names:
                client.send('005.1'.encode(transmision_type))
                new_name = client.recv(1024).decode(transmision_type)
                print(f'Server: {address[0]}:{address[1]} tried to create an account, but unsuccessfully')
                if new_name not in client_log.names:
                    client.send('005.2'.encode(transmision_type))
                    break
                
            client.send('005.2'.encode(transmision_type))
            client_log.current_name = new_name
            client_log.Login = True

            f_names_a = open('names.txt', 'a')
            f_names_a.write(f'{new_name}\n')
            f_passwords_a = open('passwords.txt', 'a')
            f_passwords_a.write(f'{new_password}\n')
            f_names_a.close()
            f_passwords_a.close()
            client_log.names.append(new_name)
            client_log.passwords.append(new_password)
            client_log.current_name == new_name
            client_log.Login = True
            print(f'Server: {address[0]}:{address[1]} created successfully an account with the name {new_name}.')
        


    def creating_mail(self):        
        if client_log.menu_decision == '007' and client_log.Login == True:
            o = client.recv(1024).decode(transmision_type)
            time.sleep(0.3)
            c = client.recv(1024).decode(transmision_type)
            time.sleep(0.3)
            p = client.recv(1024).decode(transmision_type)

            while o not in client_log.names:
                client.send('007.1'.encode(transmision_type))
                o = client.recv(1024).decode(transmision_type)
                time.sleep(0.3)
                c = client.recv(1024).decode(transmision_type)
                time.sleep(0.3)
                p = client.recv(1024).decode(transmision_type)
                if o in client_log.names:
                    client.send('007.2'.encode(transmision_type))
                    break
            else:
                client.send('007.2'.encode(transmision_type))


            f_messages_a = open('messages.txt', 'a')
            f_messages_a.write(f'{o}o\n{c}c\n{p}p\n')
            f_messages_a.close()
            print(f'Server: {address[0]}:{address[1]} from {client_log.current_name} created an e-mail.')
        
            

            
    def reading_mail(self):        
        if client_log.menu_decision == '008' and client_log.Login == True:
            words = ''
            counter = 0
            pocket3 = []
            for char in client_log.messages:
                pocket2 = char

                if  pocket2[1] == client_log.current_name:
                        pocket3.append(pocket2)
                        pocket2 = []
                            
                            
            for char in pocket3:
                for char1 in char:
                    if counter == 3:
                        words += '\n'
                        words += '\n'
                        counter = 0
                            
                    if counter == 2:
                        words += '\n'
                        words += '\n'
                        words += 'Message: ' + char1
                        counter += 1

                    if counter == 1:
                        words += '\n'
                        words += '\n'
                        words += "Recipient's:  " + char1
                        counter += 1

                    if counter == 0:
                        words += '================'
                        words += '\n'
                        words += '\n'
                        words += 'Sender: ' + char1
                        counter += 1

            client.send(words.encode(transmision_type))
            print(f'Server: {address[0]}:{address[1]} from {client_log.current_name} read e-mails.')
        


    def Logout(self):
        if client_log.menu_decision == '009' and client_log.Login == True:
            print(f'Server: {address[0]}:{address[1]} logout from {client_log.current_name}.')
            client_log.Login = False
            client_log.current_name = None
        
              
    
        
    def menu(self):
        while True and client_log.Exit == False:
            client_log.synchronization()
            client_log.menu_decision = client.recv(1024).decode(transmision_type)
            client_log.login()
            client_log.create_account()
            client_log.creating_mail()
            client_log.Logout()
            client_log.reading_mail()
            client_log.exit()
        
            
    
    def synchronization(self):   
        list_m_from_file = []
        addressee = ''
        recipient = ''
        message = ''
        pocket = []
        client_log.names.clear()
        client_log.passwords.clear()
        client_log.messages.clear()
        f_names_r = open('names.txt', 'r')
        f_passwords_r = open('passwords.txt', 'r')
        f_messages_r = open('messages.txt', 'r')
        
        read_f_messages = f_messages_r.readlines()

        for line in read_f_messages:
            list_m_from_file.append(line.strip())

        for char in list_m_from_file:
            if char[-1] == 'c':
                addressee = (char[:-1])
            if char[-1] == 'o':
                recipient = (char[:-1])

            if char[-1] == 'p':
                message = (char[:-1])


            if addressee != '' and recipient != '' and message != '':
                pocket.append(addressee)
                pocket.append(recipient)
                pocket.append(message)
                client_log.messages.append(pocket)
                pocket = []

                addressee = ''
                recipient = ''
                message = ''
        f_messages_r.close()


        read_f_names = f_names_r.readlines()
        for line in read_f_names:
            client_log.names.append(line.strip())
        f_names_r.close()

        read_f_passwords = f_passwords_r.readlines()
        for line in read_f_passwords:
            client_log.passwords.append(line.strip())

        f_passwords_r.close()
            

    def exit(self):
        if client_log.menu_decision == '010':
            print(f'Server: {address[0]}:{address[1]} closed app.')
            client.close()
            client_log.Login = False
            client_log.current_name = None
            client_log.Exit = True


while True:
    client , address = server.accept()
    print(f'Server: Connected with {address[0]}:{address[1]}.')
    client_log = Client(False)
    
    try:
        thread = threading.Thread(target=Client.menu(self = client_log),args=(client,client_log))
        thread.start()
    except ConnectionError:
        client_log.Login = False
        client_log.current_name = None
        client.close()
        print(f'Server: Lost connection with {address[0]}:{address[1]}.')