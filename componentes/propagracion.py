import numpy as np
from scipy.signal import convolve2d

# Definir las areas de influencia
# Cada area es una matriz de 5x5 que contiene ceros y unos. 
# Los unos indican las posiciones a las que el fuego puede propagarse desde una celda en llamas.
# Estas matrices de influencia representan en cómo se distribuyen los efectos del fuego en la simulación

# MI_0: Representa propagación en las direcciones cardinales (0 grados). En las cuatro direcciones cardinales
MI_0 = np.array([[0, 0, 0, 0, 0],
                 [0, 0, 1, 0, 0],
                 [0, 1, 0, 1, 0],
                 [0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0]])
# MI_145: Representa propagación en la dirección aproximada de 145 grados (hacia el sureste)
MI_145 = np.array([[0, 0, 0, 0, 0],
                   [0, 1, 1, 1, 0],
                   [0, 0, 0, 1, 0],
                   [0, 0, 0, 1, 0],
                   [0, 0, 0, 0, 0]])

# MI_190: Representa propagación en la dirección aproximada de 190 grados (hacia el sur-suroeste).
MI_190 = np.array([[0, 0, 0, 0, 0],
                   [0, 0, 1, 1, 0],
                   [0, 0, 0, 1, 0],
                   [0, 0, 1, 1, 0],
                   [0, 0, 0, 0, 0]])

# MI_245: Representa propagación en la dirección aproximada de 245 grados (hacia el oeste-suroeste).
MI_245 = np.array([[0, 0, 1, 1, 1],
                   [0, 0, 1, 1, 1],
                   [0, 0, 0, 1, 1],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0]])

# MI_290: Representa propagación en la dirección aproximada de 290 grados (hacia el oeste-noroeste).
MI_290 = np.array([[0, 0, 0, 0, 0],
                   [0, 0, 1, 1, 1],
                   [0, 0, 0, 1, 1],
                   [0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0]])
class ContadorIncendio:
    area_quemada = float(0)
# Función para propagar el valor 2 usando un area_influencia, con la restricción de solo propagar en valores no 0
def propagar_fuego(matriz, area_influencia, humedad):
    # Crear una copia, esto es útil para mantener una versión original de la matriz
    matriz_actualizada = matriz.copy()

    # encuentra las posiciones (índices) de las celdas en la matriz que tienen el valor 2 (celdas en llamas).
    celdas_ardiendo = np.argwhere(matriz == 2)
    celdas_con_baja_humedad = []
    # Se seleccionan solo las celdas en llamas que tienen una humedad baja (menor o igual a 0.2).
    for pos in celdas_ardiendo:
        i, j = pos
        if humedad[i][j] <= 0.2:
            celdas_con_baja_humedad.append(pos)

    for (i, j) in celdas_con_baja_humedad:
        # Crear una matriz temporal con un 2 en la posición del 2
        matriz_temp = np.zeros_like(matriz)
        matriz_temp[i, j] = 2

        # echar la convolución con el area_influencia
        conv_resultado = convolve2d(matriz_temp, area_influencia, mode='same', boundary='fill', fillvalue=0)

        # Propagar el valor 2 solo en celdas donde matriz original no sea 0
        mask = (matriz != 0) * humedad
        conv_resultado = np.where(mask >= 0.65, conv_resultado, 0)

        # Actualizar el matriz_actualizada con la propagación válida
        matriz_actualizada = np.maximum(matriz_actualizada, conv_resultado)

    for (i, j) in celdas_ardiendo:
        if humedad[i, j] != 0:
            matriz_actualizada[i, j] = 2
            humedad[i, j] = max(0, humedad[i, j] - 0.05)

        if humedad[i, j] == 0:
            matriz_actualizada[i, j] = 0
            ContadorIncendio.area_quemada += 0.056
            print(ContadorIncendio.area_quemada)
        else:
            matriz_actualizada[i, j] = 2

    return matriz_actualizada


def echar_agua(matriz, area_influencia, posicion, matriz_fuego):
    tamano_area = area_influencia.shape[0]
    desplazamiento = tamano_area // 2
    x, y = posicion
    matriz_actualizada = matriz.copy()

    # Iterar sobre el área de influencia y la matriz de salida para echar los valores
    for i in range(tamano_area):
        for j in range(tamano_area):
            if area_influencia[i, j] == 1:
                nueva_x, nueva_y = x + i - desplazamiento, y + j - desplazamiento
                if 0 <= nueva_x < matriz.shape[0] and 0 <= nueva_y < matriz.shape[1]:
                    if matriz_fuego[nueva_x][nueva_y] == 2:  # Si la celda está en llamas
                        matriz_fuego[nueva_x][nueva_y] = 0  # Extinguir el fuego
                        ContadorIncendio.area_quemada += 0.056
                        print(ContadorIncendio.area_quemada)
                    matriz_actualizada[nueva_x][nueva_y] = 1  # echar agua a la celda
    matriz_actualizada[x][y] = 1  # echar agua a la celda original

    return matriz_actualizada
