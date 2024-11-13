import requests
from PIL import Image, ImageTk
import io

def descargar_imagen(url, size):
    """
    Descarga una imagen desde una URL, la redimensiona al tamaño especificado, y la convierte en un formato compatible con Tkinter.

    Parámetros:
        url (str): La URL de la imagen a descargar.
        size (tuple): Tamaño al que se redimensionará la imagen, en píxeles (ancho, alto).

    Retorno:
        ImageTk.PhotoImage: La imagen descargada y redimensionada en un formato compatible con Tkinter,
                            o None si la descarga falla.
    """
    try:
        # Realiza una solicitud GET para descargar la imagen desde la URL
        response = requests.get(url)
        response.raise_for_status()  # Verifica si la solicitud fue exitosa

        # Abre la imagen desde los datos descargados
        image_data = io.BytesIO(response.content)
        image = Image.open(image_data)

        # Redimensiona la imagen
        image = image.resize(size, Image.LANCZOS)

        # Convierte la imagen a un formato compatible con Tkinter y la devuelve
        return ImageTk.PhotoImage(image)

    except requests.RequestException as e:
        # Si ocurre un error en la solicitud, muestra un mensaje de error y devuelve None
        print(f"Error al descargar la imagen desde {url}: {e}")
        return None
