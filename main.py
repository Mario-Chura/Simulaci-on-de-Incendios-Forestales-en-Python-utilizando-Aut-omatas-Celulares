import tkinter as tk
from tkinter import ttk
from componentes.propagracion import *
from componentes.entorno import *
from componentes.estados import estados
import numpy as np
from PIL import Image, ImageTk

# Variables globales
grid, humedad_grid = None, None
estado_inicial, humedad_inicial = None, None
area_influencia = MI_0
velocidad = 0
modo_agua = False
vista_humedad = False
pausado = False
ejecutando = True
ancho, alto = 1200, 700
tamanio_grid = [alto // 10, ancho // 10]

def inicializar_simulacion():
    global grid, humedad_grid, estado_inicial, humedad_inicial
    # Crear matriz a partir de una imagen
    grid, humedad_grid = espacio_imagen(imagen_a_matriz_rgb('nuevo.jpg'))
    estado_inicial = grid.copy()
    humedad_inicial = humedad_grid.copy()
    
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def iniciar_incendio(event):
    global grid
    x, y = event.y // (alto // tamanio_grid[0]), event.x // (ancho // tamanio_grid[1])
    if modo_agua:
        if grid[x, y] == 2:  # Verifica si la celda está ardiendo (roja)
            grid[x, y] = 0  # Apaga el incendio
    elif grid[x, y] == 1:  # Verifica si la celda está viva (verde)
        grid[x, y] = 2  # Inicia el incendio

def actualizar_simulacion():
    global grid, humedad_grid
    if not pausado:
        if not vista_humedad:
            next_grid = propagar_fuego(grid, area_influencia, humedad_grid)
            grid = next_grid
        canvas.delete("all")
        for x in range(tamanio_grid[0]):
            for y in range(tamanio_grid[1]):
                # Asegúrate de que las celdas muertas se pinten de negro
                if grid[x, y] == 0:
                    color = (0, 0, 0)  # Negro
                elif not vista_humedad:
                    color = estados[grid[x, y]]
                else:
                    color = obtener_color_por_valor(humedad_grid[x, y])
                
                color_hex = rgb_to_hex(tuple(color))
                canvas.create_rectangle(y * ancho // tamanio_grid[1], x * alto // tamanio_grid[0],
                                        (y + 1) * ancho // tamanio_grid[1], (x + 1) * alto // tamanio_grid[0],
                                        fill=color_hex)
    root.after(100, actualizar_simulacion)

def pausar():
    global pausado
    pausado = not pausado
    btn_pausa.config(text="Continuar" if pausado else "Pausa")

def reset():
    global grid, humedad_grid
    grid = estado_inicial.copy()
    humedad_grid = humedad_inicial.copy()
    ContadorIncendio.area_quemada = 0

def toggle_agua():
    global modo_agua
    modo_agua = not modo_agua
    btn_toggle_agua.config(text="Modo Echar Agua (ON)" if modo_agua else "Modo Echar Agua (OFF)")

def toggle_humedad():
    global vista_humedad
    vista_humedad = not vista_humedad
    btn_toggle_humedad.config(text="Vista Humedad (ON)" if vista_humedad else "Vista Humedad (OFF)")

def set_velocidad(val):
    global velocidad, area_influencia
    velocidad = int(val)
    area_influencia = [MI_0,MI_0,MI_0][velocidad]

def set_direccion(direccion):
    global area_influencia
    direcciones = {
        "up": np.rot90(MI_190, k=1) if velocidad == 1 else np.rot90(MI_290, k=1),
        "down": np.rot90(MI_190, k=-1) if velocidad == 1 else np.rot90(MI_290, k=-1),
        "left": np.rot90(MI_190, k=2) if velocidad == 1 else np.rot90(MI_290, k=2),
        "right": MI_190 if velocidad == 1 else MI_290,
    }
    area_influencia = direcciones[direccion]

root = tk.Tk()
root.title("Simulación de Incendios Forestales")
root.geometry(f"{ancho}x{alto}")

canvas = tk.Canvas(root, width=ancho * 0.7, height=alto)
canvas.pack(side=tk.LEFT)
canvas.bind("<Button-1>", iniciar_incendio)

frame = tk.Frame(root)
frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 20))

btn_pausa = tk.Button(frame, text="Pausa", command=pausar)
btn_pausa.pack(pady=5)
btn_reset = tk.Button(frame, text="Reiniciar", command=reset)
btn_reset.pack(pady=5)
btn_toggle_agua = tk.Button(frame, text="Modo Echar Agua (OFF)", command=toggle_agua)
btn_toggle_agua.pack(pady=5)
btn_toggle_humedad = tk.Button(frame, text="Vista Humedad (OFF)", command=toggle_humedad)
btn_toggle_humedad.pack(pady=5)

label_velocidad = tk.Label(frame, text="Velocidad del aire")
label_velocidad.pack(pady=5)
radio_frame = tk.Frame(frame)
radio_frame.pack()
velocidad_var = tk.StringVar(value="0")
tk.Radiobutton(radio_frame, text="0", variable=velocidad_var, value="0", command=lambda: set_velocidad(0)).pack(side=tk.LEFT)
tk.Radiobutton(radio_frame, text="1", variable=velocidad_var, value="1", command=lambda: set_velocidad(1)).pack(side=tk.LEFT)
tk.Radiobutton(radio_frame, text="2", variable=velocidad_var, value="2", command=lambda: set_velocidad(2)).pack(side=tk.LEFT)

label_direccion = tk.Label(frame, text="Dirección del aire")
label_direccion.pack(pady=10)
dir_frame = tk.Frame(frame)
dir_frame.pack()
tk.Button(dir_frame, text="↑", command=lambda: set_direccion("up")).pack()
tk.Button(dir_frame, text="←", command=lambda: set_direccion("left")).pack(side=tk.LEFT)
tk.Button(dir_frame, text="→", command=lambda: set_direccion("right")).pack(side=tk.RIGHT)
tk.Button(dir_frame, text="↓", command=lambda: set_direccion("down")).pack()

inicializar_simulacion()
actualizar_simulacion()
root.mainloop()
