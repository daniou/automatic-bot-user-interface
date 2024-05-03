import pygetwindow as gw

# Título de la ventana a encontrar
window_title = "TallerPro"

# Obtener la ventana con el título especificado
window = gw.getWindowsWithTitle(window_title)

if window:
    # Obteniendo la primera ventana encontrada
    window = window[0]
    print("Ventana encontrada. Moviendo la ventana...")

    # Nuevas coordenadas para mover la ventana
    new_x = 0  # Nueva posición en el eje X
    new_y = 100  # Nueva posición en el eje Y

    # Moviendo la ventana a las nuevas coordenadas
    window.moveTo(new_x,new_y)
    print("Ventana movida a la posición:", new_x, new_y)
else:
    print(f"No se encontró ninguna ventana con el título '{window_title}'.")
