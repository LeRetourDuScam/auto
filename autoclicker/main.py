import pyautogui
import time

def main():
    print("Bienvenue dans l'auto-clicker !")
    interval = float(input("Entrez l'intervalle entre les clics (en secondes) : "))
    print("L'auto-clicker commence. Appuyez sur Ctrl+C pour arrêter.")
    try:
        while True:
            pyautogui.click()  # Clic de la souris
            time.sleep(interval)  # Pause entre chaque clic
    except KeyboardInterrupt:
        print("\nL'auto-clicker a été arrêté.")
