import socket
import threading
import time

# Configuration du serveur
HOST = '127.0.0.1'
PORT1 = 34600
PORT2 = 34500
data_port1 = ''
received_data1 = ''
state_brackets_chain = ''

def brackets_verif():
    global received_data1
    global state_brackets_chain

    i=0
    for bracket in received_data1:
        if bracket == '[':
            i+=1
        elif bracket == ']':
            i-=1
    if i != 0:
        state_brackets_chain = 'O'
        #print(state_brackets_chain)
    else:
        state_brackets_chain = 'F'
        #print(state_brackets_chain)

def start_server_port_34600():
    global data_port1
    global received_data1
    global state_brackets_chain

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT1))
        server_socket.listen()
        print(f"Serveur en écoute sur le port {PORT1}")

        # Accepter une connexion
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connexion établie avec {addr} sur le port {PORT1}")            
            while True:
                # Recevoir des données (1024 bytes à la fois)
                data_port1 = conn.recv(1024)
                received_data1 = data_port1.decode('utf-8')
                if not data_port1:
                    break  # Si aucune donnée reçue, quitter la boucle        
                brackets_verif()        
                print(f"Chaine : {received_data1} ==> {state_brackets_chain}")
            print(f"Connexion du port {PORT1} fermée.")


def send_answer():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sender_socket:
        sender_socket.connect((HOST, PORT2))
        while True:
            sender_socket.sendall(state_brackets_chain.encode('utf-8'))  # Envoi de la réponse
            time.sleep(1)

ouverture_port_34600=threading.Thread(target=start_server_port_34600)
envoie_reponse_34500=threading.Thread(target=send_answer)

ouverture_port_34600.start()
envoie_reponse_34500.start()