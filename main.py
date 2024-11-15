import tkinter as tk
from controlador import GameController  # Asegúrate de tener GameController en controlador.py
from modelo import GameModel  # Asegúrate de tener GameModel en modelo.py

if __name__ == "__main__":
    # Inicialización de la ventana principal
    root = tk.Tk()
    root.title("Juego de Memoria")

    # Inicialización del modelo del juego
    # Aquí puedes definir la dificultad inicial y el nombre del jugador
    # Por ejemplo, dificultad "normal" y jugador "Anónimo"
    model = GameModel(difficulty="fácil", player_name="Jacobo")

    # Inicialización del controlador del juego
    # El controlador manejará el flujo y lógica del juego
    controller = GameController(root, model)

    # Bucle principal de Tkinter para mantener la aplicación activa
    root.mainloop()
