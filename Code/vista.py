import tkinter as tk
from tkinter import simpledialog, Toplevel, Label
from tkinter import ttk


class GameView:
    def __init__(self, on_card_click_callback, update_move_count_callback, update_time_callback):
        # Inicializamos los callbacks
        self.on_card_click_callback = on_card_click_callback
        self.update_move_count_callback = update_move_count_callback
        self.update_time_callback = update_time_callback

        # Crea una nueva ventana TopLevel para el tablero de juego
        self.window = Toplevel()
        self.window.title("Juego de Memoria")

        # Inicializamos los atributos para la vista
        self.labels = {}
        self.move_label = Label(self.window, text="Movimientos: 0", font=("Helvetica", 12))
        self.time_label = Label(self.window, text="Tiempo: 0", font=("Helvetica", 12))

        self.hidden_image = None

    def create_board(self, model):
        """Crea el tablero de juego en una nueva ventana (Toplevel)."""
        self.labels = {}  # Limpiamos las etiquetas anteriores si existen
        self.hidden_image = model.hidden_image

        # Crea un grid de etiquetas para representar las cartas en el tablero
        for i in range(model.board_size):
            for j in range(model.board_size):
                pos = (i, j)
                label = Label(self.window, width=66, height=100, relief="raised", bg="gray")
                label.grid(row=i, column=j, padx=5, pady=5)
                label.config(image=self.hidden_image)
                label.image = self.hidden_image  # Actualiza la referencia a la imagen
                # Asignamos una función de callback para el clic de cada carta
                label.bind("<Button-1>", lambda event, p=pos: self.on_card_click_callback(p))
                self.labels[pos] = label

        # Etiquetas para el contador de movimientos y el temporizador
        self.move_label.grid(row=model.board_size, column=0, columnspan=model.board_size, pady=10)
        self.time_label.grid(row=model.board_size + 1, column=0, columnspan=model.board_size, pady=10)

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

        if label1:
            label1.config(image=self.hidden_image)
            label1.image = self.hidden_image  # Actualiza la referencia a la imagen
        if label2:
            label2.config(image=self.hidden_image)
            label2.image = self.hidden_image  # Actualiza la referencia a la imagen

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


class LoadingWindow:
    def __init__(self, root, total_images):
        self.window = tk.Toplevel(root)
        self.window.title("Cargando imágenes")
        self.window.geometry("300x150")
        self.window.resizable(False, False)

        self.label = tk.Label(self.window, text="Descargando imágenes...")
        self.label.pack(pady=10)

        self.progress = ttk.Progressbar(self.window, orient="horizontal", length=250, mode="determinate")
        self.progress.pack(pady=20)

        self.total_images = total_images
        self.current_progress = 0
        self.progress["maximum"] = total_images

    def update_progress(self, value):
        self.current_progress += value
        self.progress["value"] = self.current_progress
