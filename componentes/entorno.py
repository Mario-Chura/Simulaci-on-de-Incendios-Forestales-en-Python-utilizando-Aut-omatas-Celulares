from PIL import Image  
import numpy as np  
# Cargamos una imagen y la convertimos a una matriz RGB
def imagen_a_matriz_rgb(ruta_imagen):
    try:
        # Abrimos la imagen
        imagen = Image.open(ruta_imagen)
    except IOError as e:
        print(f"Error al abrir la imagen: {e}")
        return None
    
    # Convetimos a formato RGB
    imagen = imagen.convert("RGB")
    
    # Obtiene el ancho y alto de la imagen
    ancho, alto = imagen.size
    
    # Creamos una matriz vacía de ceros con las dimensiones de la imagen
    matriz = np.zeros((alto, ancho, 3), dtype=np.uint8)
    
    # Recorre cada píxel de la imagen y lo asigna a la matriz
    for y in range(alto):
        for x in range(ancho):
            matriz[y, x] = imagen.getpixel((x, y))
    
    return matriz

# Convertimos un color RGB a un valor específico
def asignar_valor_por_rgb(color):
    r, g, b = color  
    checks = [
        (g > 150, 1),
        (b > 100, 5),
    ]
    for check, value in checks:
        if check:
            return value
    return 0 


# Convertimos un estado de color a un valor de humedad
def humedad_segun_estado(estado):

    humedad_limites = [0.2, 0.4]

    humedades_fijas = {
        0: 1,  # Células muertas
        5: 1   # Agua
    }
    
    # Humedad de 100% para celulas muertas y agua
    if estado in humedades_fijas:
        return humedades_fijas[estado]
    
    # Humedad aleatoria para otros estados
    min_humedad = 1 - humedad_limites[1]  # 1 - 0.4 = 0.6
    max_humedad = 1 - humedad_limites[0]  # 1 - 0.2 = 0.8
    return np.random.uniform(min_humedad, max_humedad)


# Procesamos la matriz RGB y generar matrices de valores y humedad
def espacio_imagen(matriz):
    alto, ancho, _ = matriz.shape  
    matriz_grid = np.zeros((alto, ancho), dtype=np.uint8)  
    matriz_humedad = np.zeros((alto, ancho))  
    for y in range(alto):  
        for x in range(ancho):
            # Obetenemos el color del píxel en la posición (x, y)  
            color = matriz[y, x]
            # Convierte el color a un valor y lo asigna a la matriz  
            matriz_grid[y, x] = asignar_valor_por_rgb(color) 
            # Convierte el valor a humedad y lo asigna
            matriz_humedad[y, x] = humedad_segun_estado(matriz_grid[y, x])  
    #Contamos e imprimimos el número de celdas que tienen un estado diferente de 0
    print(np.sum(matriz_grid != 0))  
    return matriz_grid, matriz_humedad  

def clic_a_posicion(x, y):
    posx = y // 10  
    posy = x // 10 
    return posx, posy 


# Función para obtener el gradiente de color Azul-Blanco para graficar la humedad
def obtener_color_por_valor(valor):
    assert 0 <= valor <= 1, "El valor debe estar entre 0 y 1"  

    azul = [0, 0, 255]  
    blanco = [255, 255, 255] 

    # Calcular la interpolación entre azul y blanco
    rojo = int(valor * blanco[0] + (1 - valor) * azul[0])
    verde = int(valor * blanco[1] + (1 - valor) * azul[1])
    azul = int(valor * blanco[2] + (1 - valor) * azul[2])

    # Combina los componentes en un array numpy
    color = np.array([rojo, verde, azul])  
    return color 
