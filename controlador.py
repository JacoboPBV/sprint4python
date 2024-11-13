from tkinter import messagebox, simpledialog, Toplevel, Label

from modelo import GameModel
from vista import MainMenu, GameView  # Asumiendo que MainMenu y GameView están en vista.py

class GameController:
    def __init__(self, root, modelo):
        self.root = root
        self.model: GameModel = modelo
        self.selected = []
        self.timer_started = False

        # Crear la vista
        self.game_view: GameView = None
        self.main_menu: MainMenu = MainMenu(root, self.start_game, self.show_stats, self.quit_game)

    def show_difficulty_selection(self):
        # Diálogo para elegir la dificultad
        difficulty = simpledialog.askstring("Seleccionar Dificultad", "Escribe la dificultad (fácil, medio, difícil):")
        if difficulty in ["fácil", "medio", "difícil"]:
            player_name = simpledialog.askstring("Nombre del Jugador", "Escribe tu nombre:")
            if player_name:
                self.start_game()
            else:
                messagebox.showerror("Error", "Debe ingresar un nombre de jugador.")
        else:
            messagebox.showerror("Error", "Dificultad no válida.")

    def start_game(self):
        # Muestra la ventana de carga y crea una instancia del modelo de juego
        self.show_loading_window("Cargando el tablero...")
        self.check_images_loaded()
        if self.game_view is not None:
            self.game_view.create_board(self.model.board_size)

    def quit_game(self):
        """Cierra la aplicación."""
        self.root.quit()  # Detiene el bucle de eventos de Tkinter

    def show_loading_window(self, message):
        # Ventana de carga
        self.loading_window = Toplevel(self.root)
        self.loading_window.title("Cargando")
        Label(self.loading_window, text=message).pack()
        self.loading_window.transient(self.root)
        self.loading_window.grab_set()

    def check_images_loaded(self):
        # Verifica si las imágenes han terminado de cargar
        if self.model.images_are_loaded():
            self.loading_window.destroy()
            self.game_view = GameView(self.on_card_click, 0, self.update_time)
        else:
            self.root.after(100, self.check_images_loaded)

    def on_card_click(self, pos):
        # Evento al hacer clic en una carta
        if not self.timer_started:
            self.model.start_timer()
            self.timer_started = True

        self.selected.append(pos)
        self.game_view.update_board(pos, self.model.images.get(0))

        if len(self.selected) == 2:
            self.handle_card_selection()

    def handle_card_selection(self):
        # Verifica si las cartas seleccionadas coinciden
        pos1, pos2 = self.selected
        if self.model.check_match(pos1, pos2):
            self.check_game_complete()
        else:
            self.root.after(500, lambda: self.game_view.reset_cards(pos1, pos2))
        self.update_move_count(self.model.moves)
        self.selected = []

    def update_move_count(self, moves):
        # Actualiza el contador de movimientos
        self.game_view.update_move_count(moves)

    def check_game_complete(self):
        # Verifica si el juego se ha completado
        if self.model.is_game_complete():
            self.model.save_score()
            messagebox.showinfo("¡Victoria!", f"¡Felicidades {self.model.player_name}! Completaste el juego en {self.model.moves} movimientos y {self.model.get_time()} segundos.")
            self.return_to_main_menu()

    def return_to_main_menu(self):
        # Vuelve al menú principal
        self.game_view.destroy()

    def show_stats(self):
        # Muestra las estadísticas de puntuación
        scores = self.model.load_scores()
        message = "Ranking:\n"
        for difficulty, score_list in scores.items():
            message += f"\n{difficulty.capitalize()}:\n"
            for entry in score_list:
                message += f"{entry['nombre']}: {entry['movimientos']} movimientos en {entry['fecha']}\n"
        messagebox.showinfo("Estadísticas", message)

    def update_time(self):
        # Actualiza el temporizador en la vista de juego
        if self.timer_started and self.model:
            self.game_view.update_time(self.model.get_time())
            self.root.after(1000, self.update_time)
