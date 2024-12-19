import socket
import threading
import time
import random

# Configuration du serveur
HOST = '127.0.0.1'
PORT1 = 34600
PORT2 = 34500
data_port2 = ''
random_brackets = ''
state_brackets_chain = ''
nb_point = 0
last_response_time = 0
response_cooldown = 1

def brackets_verif():
    global random_brackets
    global state_brackets_chain
    i=0
    for bracket in random_brackets:
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


def send_random_brackets():
    global random_brackets
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sender_socket:
                print(f"Tentative de connexion à {HOST}:{PORT1}...")
                sender_socket.connect((HOST, PORT1))
                print("Connexion établie!")
                while True:
                    # Générer une chaîne de 20 crochets aléatoires
                    random_brackets = ''.join(random.choice(['[', ']']) for _ in range(20))
                    send_line = random_brackets
                    brackets_verif()
                    sender_socket.sendall(send_line.encode('utf-8'))  # Envoi de la chaîne
                    time.sleep(1)
        except ConnectionRefusedError:
                print(f"Connexion échouée, le serveur sur {HOST}:{PORT1} n'est pas encore disponible.")
                time.sleep(5)  # Réessayer toutes les 5 secondes en cas d'échec
        except Exception as e:
                print(f"Erreur : {e}")
                time.sleep(5)  # Attendre avant de réessayer en cas d'autres erreurs



def start_server_port2():
    global data_port2
    global state_brackets_chain
    global nb_point
    global last_response_time

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT2))
        server_socket.listen()
        print(f"Serveur en écoute sur le port {PORT2}")

        # Accepter une connexion
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connexion établie avec {addr} sur le port {PORT2}")            
            while True:
                if nb_point < 50:
                    data_port2 = conn.recv(1024)
                    received_data_port2 = data_port2.decode('utf-8').strip()
                    if not data_port2:
                        break
                    print(f"Données reçues : {received_data_port2}")
                    
                    current_time = time.time()
                    # Vérifie si le cooldown est respecté
                    if current_time - last_response_time < response_cooldown:
                        print("Attendez un peu avant d'envoyer une nouvelle réponse.")
                        continue
                    
                    if received_data_port2 == state_brackets_chain:
                        nb_point += 1
                        last_response_time = current_time
                        if nb_point == 1:
                            print(f"Bonne réponse, vous avez {nb_point} point !")
                        else:
                            print(f"Bonne réponse, vous avez {nb_point} points !")
                    else:
                        nb_point = 0
                        print(f"Mauvaise réponse, on retourne à zéro !")
                else:
                    print("Tu as gagné ! ==> Q1RGLURMUygxX1B0aXRfV3I0cCEhISk=")
                    break
            print(f"Connexion du port {PORT2} fermée.")
            




#Lancement de l'ecoute sur le port 34500 et 34600 et de l'envoie des crochets sur 34600
thread34500 = threading.Thread(target=start_server_port2)
thread34600_send_brackets = threading.Thread(target=send_random_brackets)


thread34500.start()
thread34600_send_brackets.start()
print("GL HF !\nTu dois avoir 50 bonnes réponses")