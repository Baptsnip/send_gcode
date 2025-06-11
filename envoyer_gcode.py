
import serial
import time

def envoyer_fichier_gcode(port_usb: str, baudrate: int, chemin_fichier: str, taille_buffer: int = 10):
    """
    Envoie un fichier G-code par morceaux via un port série USB, avec gestion du buffer de réception.

    :param port_usb: Port série (ex: COM3 sous Windows ou /dev/ttyUSB0 sous Linux)
    :param baudrate: Vitesse de transmission (ex: 115200)
    :param chemin_fichier: Chemin du fichier G-code à envoyer
    :param taille_buffer: Nombre de lignes envoyées avant d'attendre un accusé de réception
    """
    try:
        # Ouverture de la connexion série
        with serial.Serial(port_usb, baudrate, timeout=1) as ser:
            print(f"Connexion au port série {port_usb} à {baudrate} bauds...")
            time.sleep(2)  # Attente pour laisser le temps au microcontrôleur de s'initialiser
            print("Connecté avec succès !")

            # Ouverture du fichier G-code
            with open(chemin_fichier, 'r') as fichier_gcode:
                buffer = []  # Buffer temporaire pour stocker les lignes
                for ligne in fichier_gcode:
                    ligne = ligne.strip()  # Suppression des espaces et retours à la ligne
                    if ligne:
                        buffer.append(ligne)

                        # Si le buffer atteint la taille définie, on envoie le lot
                        if len(buffer) >= taille_buffer:
                            for cmd in buffer:
                                ser.write((cmd + '\n').encode('utf-8'))  # Envoi de chaque ligne
                                print(f"Envoyé: {cmd}")
                            buffer.clear()  # Vider le buffer après l'envoi

                            # Attente d'une réponse (accusé de réception, typiquement 'ok')
                            reponse = ""
                            while True:
                                if ser.in_waiting:
                                    reponse += ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
                                    if 'ok' in reponse.lower():
                                        break
                                time.sleep(0.01)

                # Envoi des lignes restantes dans le buffer (s'il y en a)
                for cmd in buffer:
                    ser.write((cmd + '\n').encode('utf-8'))
                    print(f"Envoyé: {cmd}")

                # Dernière attente d'accusé de réception après le dernier envoi
                reponse = ""
                while True:
                    if ser.in_waiting:
                        reponse += ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
                        if 'ok' in reponse.lower():
                            break
                    time.sleep(0.01)

            print("Fichier G-code envoyé avec succès.")

    except FileNotFoundError:
        # Gestion de l'erreur si le fichier G-code n'existe pas
        print(f"Erreur : le fichier '{chemin_fichier}' est introuvable.")
    except serial.SerialException as e:
        # Gestion des erreurs liées au port série
        print(f"Erreur série : {e}")
    except Exception as e:
        # Gestion des autres erreurs imprévues
        print(f"Erreur inattendue : {e}")

if __name__ == "__main__":
    # Demande à l'utilisateur les paramètres de connexion et le chemin du fichier
    port_usb = input("Entrez le port USB (ex: COM3 ou /dev/ttyUSB0) : ")
    baudrate = int(input("Entrez le baudrate (ex: 115200) : "))
    chemin_fichier = input("Entrez le chemin du fichier G-code : ")

    envoyer_fichier_gcode(port_usb, baudrate, chemin_fichier)
