import tkinter as tk
from tkinter import simpledialog, Toplevel, Label
from recursos import descargar_imagen


class GameView:
    def __init__(self, on_card_click_callback, update_move_count_callback, update_time_callback):
        # Inicializamos los callbacks
        self.on_card_click_callback = on_card_click_callback
        self.update_move_count_callback = update_move_count_callback
        self.update_time_callback = update_time_callback

        # Inicializamos los atributos para la vista
        self.window = None
        self.labels = {}
        self.time_label = None
        self.move_label = None

    def create_board(self, board_size):
        """Crea el tablero de juego en una nueva ventana (Toplevel)."""
        # Crea una nueva ventana TopLevel para el tablero de juego
        self.window = Toplevel()
        self.window.title("Juego de Memoria")
        self.labels = {}  # Limpiamos las etiquetas anteriores si existen

        # Crea un grid de etiquetas para representar las cartas en el tablero
        for i in range(board_size):
            for j in range(board_size):
                pos = (i, j)
                label = Label(self.window, width=10, height=5, relief="raised", bg="gray")
                label.grid(row=i, column=j, padx=5, pady=5)
                # Asignamos una función de callback para el clic de cada carta
                label.bind("<Button-1>", self.on_card_click_callback(pos))
                self.labels[pos] = label

        # Etiquetas para el contador de movimientos y el temporizador
        self.move_label = Label(self.window, text="Movimientos: 0", font=("Helvetica", 12))
        self.move_label.grid(row=board_size, column=0, columnspan=board_size, pady=10)

        self.time_label = Label(self.window, text="Tiempo: 0", font=("Helvetica", 12))
        self.time_label.grid(row=board_size + 1, column=0, columnspan=board_size, pady=10)

    def update_board(self, pos, image_id):
        """Actualiza la imagen de la carta en una posición específica."""
        label = self.labels.get(pos)
        if label:
            label.config(image=image_id)
            label.image = image_id  # Mantener una referencia a la imagen para evitar que se recoja por el garbage collector

    def reset_cards(self, pos1, pos2):
        """Restaura las imágenes de dos cartas a su estado oculto."""
        label1 = self.labels.get(pos1)
        label2 = self.labels.get(pos2)
        hidden_image = descargar_imagen("https://raw.githubusercontent.com/JacoboPBV/ampliacionTkinter/refs/heads/main/fotoEjemplo.jpg", (1, 1))  # Obtiene la imagen oculta

        if label1:
            label1.config(image=hidden_image)
            label1.image = hidden_image  # Actualiza la referencia a la imagen
        if label2:
            label2.config(image=hidden_image)
            label2.image = hidden_image  # Actualiza la referencia a la imagen

    def update_move_count(self, moves):
        """Actualiza el contador de movimientos en la interfaz."""
        self.move_label.config(text=f"Movimientos: {moves}")

    def update_time(self, time):
        """Actualiza el temporizador en la interfaz."""
        self.time_label.config(text=f"Tiempo: {time}")

    def destroy(self):
        """Cierra la ventana de juego y limpia las referencias a los elementos."""
        if self.window:
            self.window.destroy()
            self.window = None
        self.labels.clear()


class MainMenu:
    def __init__(self, root, start_game_callback, show_stats_callback, quit_callback):
        """Inicializa la ventana principal del menú y establece su título."""
        self.window = root
        self.window.title("Menú Principal - Juego Memoria")

        # Crear los botones y asignarles sus respectivas funciones de callback
        tk.Button(self.window, text="Jugar", command=start_game_callback).pack(pady=10)
        tk.Button(self.window, text="Estadísticas", command=show_stats_callback).pack(pady=10)
        tk.Button(self.window, text="Salir", command=quit_callback).pack(pady=10)

    def ask_player_name(self):
        """Solicita el nombre del jugador mediante un cuadro de diálogo."""
        player_name = simpledialog.askstring("Nombre del Jugador", "Introduce tu nombre:")
        return player_name

    def show_stats(self, stats):
        """Muestra las estadísticas de los jugadores en una ventana Toplevel."""
        stats_window = Toplevel(self.window)
        stats_window.title("Estadísticas del Juego")

        # Mostrar las puntuaciones organizadas por dificultad
        for idx, (difficulty, scores) in enumerate(stats.items()):
            Label(stats_window, text=f"Dificultad: {difficulty.capitalize()}", font=("Helvetica", 14, "bold")).grid(
                row=idx * 6, column=0, sticky="w", padx=10)

            # Mostrar las mejores puntuaciones para cada dificultad
            for i, (name, moves, date) in enumerate(scores):
                score_text = f"{name} - {moves} movimientos ({date})"
                Label(stats_window, text=score_text, font=("Helvetica", 12)).grid(row=idx * 6 + i + 1,
                                                                                  column=0, sticky="w", padx=20)

        # Botón para cerrar la ventana de estadísticas
        tk.Button(stats_window, text="Cerrar", command=stats_window.destroy).grid(row=len(stats) * 6 + 1,
                                                                                  column=0, pady=10)
