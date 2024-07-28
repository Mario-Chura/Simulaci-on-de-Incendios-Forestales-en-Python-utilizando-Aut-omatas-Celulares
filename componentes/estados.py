# Representa el color de las células vivas, es decir, las áreas del bosque que no están ardiendo ni muertas. Es un tono de verde.
VIVO = (112, 168, 19)
# Representa el color de las células muertas, o áreas quemadas, y es negro.
MUERTO = (0, 0, 0)
# Representa el color de las células que están ardiendo actualmente, y es rojo.
ARDIENDO = (255, 0, 0)
# Representa el color de las células que están húmedas, probablemente debido a la aplicación de agua, y es un tono de azul claro.
HUMEDO = (0, 113, 254)
# Representa el color del agua, y es azul.
AGUA = (0, 0, 255)

estados = {
    0: MUERTO,    # Representa células muertas o áreas quemadas
    1: VIVO,      # Representa células vivas
    2: ARDIENDO,  # Representa células que están ardiendo
    4: HUMEDO,    # Representa células húmedas
    5: AGUA       # Representa agua
}
