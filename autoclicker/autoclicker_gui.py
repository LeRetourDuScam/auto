import tkinter as tk
from tkinter import ttk
import threading
import pyautogui
import time
from pynput import keyboard  # Module pour écouter globalement les événements clavier
import random  # Importer le module random

# Variables globales pour contrôler l'état du clic
clicking = False
click_thread = None
start_stop_key = None  # Variable pour stocker la touche de démarrage/arrêt
vary_interval = False  # Variable pour activer/désactiver la variation de l'intervalle
shake_cursor = False  # Variable pour activer/désactiver le tremblement du curseur

def toggle_clicking():
    """Fonction pour démarrer ou arrêter le clic"""
    global clicking
    if clicking:
        clicking = False
        status_label.config(text="Auto-clicker arrêté")
        toggle_button.config(text="Démarrer", background="green", foreground="white")
    else:
        try:
            interval = float(interval_entry.get())
        except ValueError:
            status_label.config(text="Intervalle non valide. Entrez un nombre.")
            return

        clicking = True
        # Démarrage du thread de clic
        click_thread = threading.Thread(target=click_loop, args=(interval,), daemon=True)
        click_thread.start()
        status_label.config(text="Auto-clicker démarré")
        toggle_button.config(text="Arrêter", background="red", foreground="white")

def click_loop(interval):
    """Fonction qui effectue le clic à intervalle régulier"""
    while clicking:
        if shake_cursor:
            screen_width, screen_height = pyautogui.size()
            center_x, center_y = screen_width // 2, screen_height // 2
            offset_x = random.randint(-10, 10)
            offset_y = random.randint(-10, 10)
            pyautogui.moveTo(center_x + offset_x, center_y + offset_y)
        pyautogui.click()  # Effectue un clic gauche à la position actuelle
        # Si l'intervalle est supérieur à 0, faire une pause entre les clics
        if interval > 0:
            if vary_interval:
                interval = max(0.0001, interval + random.uniform(-0.001, 0.001))  # Variation aléatoire de l'intervalle
            time.sleep(interval)
        else:
            time.sleep(0.0005)  # Pause minimale pour atteindre 2000 clics par seconde

def on_key_press(key):
    """Callback pour écouter les événements de touche globalement"""
    global start_stop_key
    try:
        key_name = key.char
    except AttributeError:
        key_name = key.name

    if start_stop_key is None:
        start_stop_key = key_name
        status_label.config(text=f"Touche de contrôle définie sur : {start_stop_key}")
    elif key_name == start_stop_key:
        toggle_clicking()

def set_key():
    """Fonction pour définir la touche de démarrage/arrêt"""
    global start_stop_key
    start_stop_key = None
    status_label.config(text="Appuyez sur la touche que vous voulez utiliser.")

def toggle_vary_interval():
    """Fonction pour activer/désactiver la variation de l'intervalle"""
    global vary_interval
    vary_interval = not vary_interval
    status_label.config(text=f"Variation de l'intervalle {'activée' if vary_interval else 'désactivée'}")
    vary_interval_button.config(text=f"Variation Intervalle {'On' if vary_interval else 'Off'}")

def toggle_shake_cursor():
    """Fonction pour activer/désactiver le tremblement du curseur"""
    global shake_cursor
    shake_cursor = not shake_cursor
    status_label.config(text=f"Tremblement du curseur {'activé' if shake_cursor else 'désactivé'}")
    shake_cursor_button.config(text=f"Tremblement Curseur {'On' if shake_cursor else 'Off'}")

# Création de l'interface graphique avec Tkinter
root = tk.Tk()
root.title("Auto-Clicker Avancé")

mainframe = ttk.Frame(root, padding="10")
mainframe.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S))

# Champ de saisie pour l'intervalle entre les clics
ttk.Label(mainframe, text="Intervalle entre les clics (secondes, 0 pour illimité):").grid(row=0, column=0, sticky=tk.W)
interval_entry = ttk.Entry(mainframe, width=10)
interval_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
interval_entry.insert(0, "0.0005")  # Valeur par défaut pour 2000 clics par seconde

# Boutons pour démarrer/arrêter l'auto-clicker et définir la touche
set_key_button = ttk.Button(mainframe, text="Définir Touche", command=set_key)
set_key_button.grid(row=1, column=0, pady=10, sticky=tk.W)

toggle_button = tk.Button(mainframe, text="Démarrer", command=toggle_clicking, background="green", foreground="white")
toggle_button.grid(row=2, column=0, pady=10, sticky=tk.W)

# Bouton pour activer/désactiver la variation de l'intervalle
vary_interval_button = ttk.Button(mainframe, text="Variation Intervalle Off", command=toggle_vary_interval)
vary_interval_button.grid(row=3, column=0, pady=10, sticky=tk.W)

# Bouton pour activer/désactiver le tremblement du curseur
shake_cursor_button = ttk.Button(mainframe, text="Tremblement Curseur Off", command=toggle_shake_cursor)
shake_cursor_button.grid(row=4, column=0, pady=10, sticky=tk.W)

# Label de statut pour afficher l'état
status_label = ttk.Label(mainframe, text="Prêt")
status_label.grid(row=5, column=0, columnspan=2, sticky=tk.W)

# Démarrage de l'écoute globale des touches
listener = keyboard.Listener(on_press=on_key_press)
listener.start()

root.mainloop()