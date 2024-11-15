import threading
import time
import random
import datetime
from recursos import descargar_imagen  # Asegúrate de tener descargar_imagen en recursos.py


class GameModel:
    def __init__(self, difficulty, player_name, cell_size=100):
        self.difficulty = difficulty
        self.player_name = player_name
        self.cell_size = cell_size
        self.start_time = 0
        self.moves = 0
        self.pairs_found = 0
        self.images_loaded = threading.Event()
        self.hidden_image = None
        self.board = []
        self.images = {}

        # Configuración del tamaño del tablero basado en la dificultad
        if self.difficulty == "fácil":
            self.board_size = 4
        elif self.difficulty == "medio":
            self.board_size = 6
        elif self.difficulty == "difícil":
            self.board_size = 8
        else:
            raise ValueError("Dificultad no válida.")

    def generate_board(self):
        # Genera pares de identificadores de imágenes y los mezcla
        num_pairs = (self.board_size ** 2) // 2
        image_ids = [f"{i + 1}" for i in range(num_pairs)] * 2  # Crear pares de imágenes
        random.shuffle(image_ids)
        self.board = [image_ids[i:i + self.board_size] for i in range(0, len(image_ids), self.board_size)]

    def load_images(self):
        # Carga las imágenes en un hilo separado
        def load():
            base_url = "https://raw.githubusercontent.com/CarlosAfundacion/juegoMazmorra/refs/heads/main/"  # URL base para las imágenes
            try:
                self.hidden_image = descargar_imagen(base_url + "oculto.png", (self.cell_size, self.cell_size))
                for img_id in set(sum(self.board, [])):  # Lista única de identificadores de imágenes
                    img_url = base_url + f"{img_id}.png"
                    print(f"Descargando imagen {img_id}")
                    self.images[img_id] = descargar_imagen(img_url, (self.cell_size, self.cell_size))
                self.images_loaded.set()  # Indica que todas las imágenes están cargadas
            except Exception as e:
                print(f"Error al cargar imágenes: {e}")

        threading.Thread(target=load, daemon=True).start()

    def images_are_loaded(self):
        # Verifica si todas las imágenes están cargadas
        return self.images_loaded.is_set()

    def start_timer(self):
        # Reinicia el temporizador del juego
        self.start_time = time.time()

    def get_time(self):
        # Calcula el tiempo en segundos desde el inicio del temporizador
        return int(time.time() - self.start_time)

    def check_match(self, pos1, pos2):
        # Verifica si dos posiciones en el tablero contienen la misma imagen
        self.moves += 1
        row1, col1 = pos1
        row2, col2 = pos2
        if self.board[row1][col1] == self.board[row2][col2]:
            self.pairs_found += 1
            print("Acierto")
            return True
        else:
            print("Fallo")
        return False

    def is_game_complete(self):
        # Verifica si todas las parejas han sido encontradas
        total_pairs = (self.board_size ** 2) // 2
        return self.pairs_found == total_pairs

    def save_score(self):
        # Guarda la puntuación del jugador en ranking.txt
        score_data = {
            "nombre": self.player_name,
            "dificultad": self.difficulty,
            "movimientos": self.moves,
            "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            # Cargar las puntuaciones actuales
            scores = self.load_scores()
            scores[self.difficulty].append(score_data)
            # Ordenar por menor número de movimientos y conservar las tres mejores puntuaciones
            scores[self.difficulty] = sorted(scores[self.difficulty], key=lambda x: x["movimientos"])[:3]

            # Guardar el archivo actualizado
            with open("ranking.txt", "w") as file:
                for difficulty, score_list in scores.items():
                    for entry in score_list:
                        file.write(f"{entry['nombre']},{difficulty},{entry['movimientos']},{entry['fecha']}\n")
        except Exception as e:
            print(f"Error al guardar la puntuación: {e}")

    def load_scores(self):
        # Carga y devuelve las puntuaciones desde ranking.txt
        scores = {"fácil": [], "medio": [], "difícil": []}
        try:
            with open("ranking.txt", "r") as file:
                for line in file:
                    nombre, dificultad, movimientos, fecha = line.strip().split(",")
                    scores[dificultad].append({
                        "nombre": nombre,
                        "dificultad": dificultad,
                        "movimientos": int(movimientos),
                        "fecha": fecha
                    })
        except FileNotFoundError:
            pass  # Si el archivo no existe, devuelve un diccionario vacío
        return scores
