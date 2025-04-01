import socket

def envoyer_fichier_gcode(ip_serveur: str, port: int, chemin_fichier: str):
    """
    Envoie un fichier G-code ligne par ligne à un serveur TCP.
    
    :param ip_serveur: Adresse IP du serveur
    :param port: Port du serveur
    :param chemin_fichier: Chemin du fichier G-code à envoyer
    """
    try:
        # Création de la connexion socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            print(f"Connexion au serveur {ip_serveur}:{port}...")
            client_socket.connect((ip_serveur, port))
            print("Connecté avec succès !")
            
            # Lecture et envoi des lignes du fichier G-code
            with open(chemin_fichier, 'r') as fichier_gcode:
                for ligne in fichier_gcode:
                    ligne = ligne.strip()  # Supprimer les espaces inutiles
                    if ligne:  # Envoyer uniquement les lignes non vides
                        client_socket.sendall((ligne + '\n').encode('utf-8'))
                        print(f"Envoyé: {ligne}")
            
            print("Fichier G-code envoyé avec succès.")

    except FileNotFoundError:
        print(f"Erreur : le fichier '{chemin_fichier}' est introuvable.")
    except ConnectionRefusedError:
        print(f"Erreur : impossible de se connecter au serveur {ip_serveur}:{port}.")
    except Exception as e:
        print(f"Erreur inattendue : {e}")

if __name__ == "__main__":
    # Paramètres du serveur
    ip_serveur = input("Entrez l'adresse IP du serveur : ")
    port = int(input("Entrez le port du serveur : "))
    chemin_fichier = input("Entrez le chemin du fichier G-code : ")

    envoyer_fichier_gcode(ip_serveur, port, chemin_fichier)
