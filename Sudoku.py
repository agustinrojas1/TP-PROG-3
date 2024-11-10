"""
ETAPAS DEL CODIGO 
1- Generación del tablero completo: 
    resolver_tablero: Esta función usa backtracking para resolver el tablero de Sudoku, llenando todas las celdas de manera que cumpla con las reglas del Sudoku. Esta es una manera común de generar un tablero completo y válido.
    generar_tablero_completo: Genera un tablero completo utilizando resolver_tablero, lo que asegura que el tablero tiene una solución válida y única.
    Eliminación de celdas:

2- eliminar_valores: Después de tener un tablero completo, esta función elimina un número determinado de celdas de manera aleatoria (el parámetro celdas_a_eliminar controla cuántas celdas se eliminan). De esta forma, el tablero sigue siendo resoluble, pero el jugador tiene que completar las celdas vacías.
    
3- Garantía de jugabilidad Como primero generamos un tablero completo y después eliminamos celdas, nos aseguramos de que el tablero tenga una única solución y sea resoluble.
"""

import random
import time  # Importar el módulo para medir el tiempo
import sys

# Crear un tablero vacío de 9x9
def crear_tablero_sudoku_vacio():
    return [[0 for _ in range(9)] for _ in range(9)]

# Función para imprimir el tablero de manera legible
def imprimir_tablero(tablero):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)  # Separa los bloques horizontales en dimensiones 3x3
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")  # Separa entre bloques de 3x3 verticalmente
            print(tablero[i][j] if tablero[i][j] != 0 else ".", end=" ")
        print()  # Nueva línea al final de cada fila

# Verificar si un número es válido en la posición (fila, col)
def es_valido(tablero, fila, col, num):
    # Verificar fila
    if num in tablero[fila]:
        return False
    
    # Verificar columna
    for i in range(9):
        if tablero[i][col] == num:
            return False
    
    # Verificar bloque de 3x3
    # Obtener las coordenadas de inicio del bloque de 3x3
    fila_inicio = (fila // 3) * 3  # Fila de inicio del bloque 3x3
    col_inicio = (col // 3) * 3    # Columna de inicio del bloque 3x3
    
    # Comprobar todas las celdas dentro del bloque 3x3
    for i in range(fila_inicio, fila_inicio + 3):
        for j in range(col_inicio, col_inicio + 3):
            if tablero[i][j] == num:
                return False
    
    return True

# Resolver el tablero de Sudoku usando backtracking con orden aleatorio
def resolver_tablero(tablero):
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0:
                # Probar números del 1 al 9 en orden aleatorio
                numeros = random.sample(range(1, 10), 9)
                for num in numeros:
                    if es_valido(tablero, fila, col, num):
                        tablero[fila][col] = num
                        if resolver_tablero(tablero):
                            return True
                        tablero[fila][col] = 0
                return False
    return True

# # Función para verificar si un tablero tiene una única solución.
# def contar_soluciones(tablero):
#     soluciones = [0]  # Usamos una lista para pasar la referencia por referencia

#     def backtrack(tablero):
#         if soluciones[0] > 1:
#             return  # Si encontramos más de una solución, dejamos de buscar
#         for fila in range(9):
#             for col in range(9):
#                 if tablero[fila][col] == 0:  # Celda vacía
#                     for num in range(1, 10):
#                         if es_valido(tablero, fila, col, num):
#                             tablero[fila][col] = num
#                             backtrack(tablero)
#                             tablero[fila][col] = 0  # Deshacer el cambio
#                     return  # Si no se puede colocar ningún número, retornamos
#         soluciones[0] += 1  # Si llegamos aquí, encontramos una solución

#     backtrack(tablero)
# return soluciones[0]

def resolver_tablero_Juego(tablero):
    global PASOS_ATRAS  # variable global
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0:  # Si la celda está vacía
                for num in range(1, 10):  # Probar los números del 1 al 9
                    if es_valido(tablero, fila, col, num):  # Si el número es válido
                        tablero[fila][col] = num  # Colocamos el número
                        if resolver_tablero(tablero):  # Llamada recursiva
                            return True
                        else: # si uno de los nodos dio falso en su resolucion, volvemos atras 
                            PASOS_ATRAS += 1 
                        tablero[fila][col] = 0  #  volvemos atras Deshacer (retroceder)
                return False  # Si no encontramos una solución válida, retrocedemos
    return True  # Si hemos llenado todo el tablero correctamente

# Generar un tablero completo de Sudoku (con una única solución)
def generar_tablero_completo():
    tablero = crear_tablero_sudoku_vacio()
    resolver_tablero(tablero)
    return tablero


# Función para mostrar la barra de carga sin salto de línea
def barra_de_carga(iterable, total, prefix='', length=40, fill='█'):
    """
    Muestra una barra de progreso en la terminal en la misma línea.
    :param iterable: El iterable que estamos procesando
    :param total: El total de iteraciones (usualmente el número de elementos en iterable)
    :param prefix: Texto que aparece antes de la barra
    :param length: Longitud de la barra
    :param fill: Carácter que llenará la barra
    """
    percent = (len(iterable) / total)
    filled_length = int(length * percent)
    bar = fill * filled_length + '-' * (length - filled_length)
    
    # Usamos sys.stdout.write para escribir en la misma línea sin hacer salto de línea
    sys.stdout.write(f'\r{prefix} |{bar}| {percent * 100:.1f}% Completado')
    sys.stdout.flush()

# Función para eliminar valores del tablero
def eliminar_valores(tablero, celdas_a_eliminar):
    celdas = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(celdas)

    #For para barra de carga (No es necesario)
    for i in range(celdas_a_eliminar):          
        # Mostrar barra de carga después de cada eliminación
        barra_de_carga(range(i + 1), celdas_a_eliminar, prefix='Creando Tablero de Juego')

        fila, col = celdas[i]
        tablero[fila][col] = 0
        

    
    sys.stdout.write('\n')  # Para mover el cursor a la siguiente línea después de la barra


    return tablero

# PRINCIPAL------------------------------------------------------------------>

# Inicialización de variables globales
PASOS_ATRAS = 0
valorDificultad = 0

# INICIO ----------------------------------------------->

# Imprimir bienvenida
print("<-- B I E N V E N I D O -->")
print("Haz empezado el juego del SUDOKU")
print("Selecciona la dificultad con la que deseas generar el tablero \n"
      "FACIL     --> Ingrese 1  \n"
      "Normal    --> Ingrese 2  \n"
      "Dificil   --> Ingrese 3 \n"
      "Diabolico --> Ingrese 666" )

# Obtener dificultad del jugador
dificultad = int(input("Ingrese Dificultad : "))
print( )

# Determinar el valor de dificultad basado en la entrada
if dificultad == 1:
    valorDificultad = 30
elif dificultad == 2:
    valorDificultad = 40
elif dificultad == 3:
    valorDificultad = 60
else:
    valorDificultad = 75

# Crear un tablero completo
tablero_completo = generar_tablero_completo()

# Eliminar algunas celdas para permitir jugar según la dificultad respetando la Unicidad resolutiva
inicio = time.time()  # Tiempo de inicio
tablero_jugable = eliminar_valores(tablero_completo, valorDificultad)
fin = time.time()  # Tiempo de fin
print(f"\nTiempo en el que se validó la unicidad del tablero: {fin - inicio:.4f} segundos")

# Mostrar el tablero jugable
imprimir_tablero(tablero_completo)

# Medir el tiempo de resolución del tablero
inicio = time.time()  # Tiempo de inicio
resuelto = resolver_tablero_Juego(tablero_jugable)
fin = time.time()  # Tiempo de fin

# Imprimir el tiempo que tardó en resolver el tablero
print(f"\nTiempo para resolver el tablero jugando con BackTracking: {fin - inicio:.4f} segundos con {PASOS_ATRAS} retrocesos en su resolución")

# Mostrar el tablero resuelto si fue posible
if resuelto:
    imprimir_tablero(tablero_jugable)
else:
    print("No se pudo resolver el tablero.")