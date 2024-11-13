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

# ========================
# Funciones de utilidades
# ========================

def crear_tablero_sudoku_vacio():
    return [[0 for _ in range(9)] for _ in range(9)]

def imprimir_tablero(tablero):
    """Imprime el tablero de Sudoku de forma legible."""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(tablero[i][j] if tablero[i][j] != 0 else ".", end=" ")
        print()

def barra_de_carga(iterable, total, prefix='', length=40, fill='█'):
    """Muestra una barra de carga en la terminal en la misma línea."""
    percent = (len(iterable) / total)
    filled_length = int(length * percent)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent * 100:.1f}% Completado')
    sys.stdout.flush()

# ========================
# Generación y Resolución
# ========================

# Verificar si un número es válido en la posición (fila, col)
def es_valido(tablero, fila, col, num):
    """Verifica si un número es válido en la posición dada."""
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

def es_valido_sudoku(tablero):
    # Verificar que cada fila contiene números del 1 al 9 sin repeticiones
    for fila in tablero:
        if not es_valido_conjunto(fila):
            return False
    
    # Verificar que cada columna contiene números del 1 al 9 sin repeticiones
    for col in range(9):
        columna = [tablero[fila][col] for fila in range(9)]
        if not es_valido_conjunto(columna):
            return False
    
    # Verificar que cada subcuadrante 3x3 contiene números del 1 al 9 sin repeticiones
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            subcuadrante = []
            for fila in range(i, i + 3):
                for col in range(j, j + 3):
                    subcuadrante.append(tablero[fila][col])
            if not es_valido_conjunto(subcuadrante):
                return False
    
    return True

def es_valido_conjunto(celdas):
    # Filtra ceros (o espacios vacíos) si el tablero está incompleto
    celdas = [celda for celda in celdas if celda != 0]
    return len(celdas) == len(set(celdas))

#SECUENCIAL
# Resolver Sudoku usando backtracking puro
def resolver_backtracking_puro(tablero):
    global PASOS_ATRAS # variable global
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0:   # Si la celda está vacía
                for num in range(1, 10):  # Probar los números del 1 al 9                        
                    if es_valido(tablero, fila, col, num):  # Si el número es válido
                        tablero[fila][col] = num  # Colocamos el número
                        if resolver_backtracking_puro(tablero):  # Llamada recursiva
                            return True
                        else: # si uno de los nodos dio falso en su resolucion, volvemos atras
                            PASOS_ATRAS += 1
                        tablero[fila][col] = 0  #  volvemos atras Deshacer (retroceder)
                return False  # Si no encontramos una solución válida, retrocedemos
    return True  # Si hemos llenado todo el tablero correctamente

# Resolver Sudoku usando backtracking con ramificación
def resolver_backtracking_con_ramificacion(tablero):
    global PASOS_ATRAS
    celda = encontrar_celda_mas_restringida(tablero)
    if not celda:
        return True
    fila, col = celda
    for num in range(1, 10):
        if es_valido(tablero, fila, col, num):
            tablero[fila][col] = num
            if resolver_backtracking_con_ramificacion(tablero):
                return True
            else:
                PASOS_ATRAS += 1
            tablero[fila][col] = 0
    return False

# Resolver Sudoku usando backtracking con poda
def resolver_backtracking_con_poda(tablero):
    global PASOS_ATRAS
    celda = encontrar_celda_mas_restringida(tablero)
    if not celda:
        return True
    fila, col = celda
    for num in obtener_opciones_validas(tablero, fila, col):
        tablero[fila][col] = num
        if resolver_backtracking_con_poda(tablero):
            return True
        else:
            PASOS_ATRAS += 1
        tablero[fila][col] = 0
    return False

#ALEATORIO
# Resolver Sudoku usando backtracking puro de forma aleatoria
def resolver_aleatorio_backtracking_puro(tablero):
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0:
                # Probar números del 1 al 9 en orden aleatorio
                numeros = random.sample(range(1, 10), 9)
                for num in numeros:
                    if es_valido(tablero, fila, col, num):
                        tablero[fila][col] = num
                        if resolver_aleatorio_backtracking_puro(tablero):
                            return True
                        tablero[fila][col] = 0              #Revisar
                return False
    return True

# Resolver Sudoku usando backtracking con ramificación de forma aleatoria
def resolver_aleatorio_backtracking_con_ramificacion(tablero):
    celda = encontrar_celda_mas_restringida(tablero)
    if not celda:
        return True
    fila, col = celda
    # Probar números del 1 al 9 en orden aleatorio
    numeros = random.sample(range(1, 10), 9)    
    for num in numeros:
        if es_valido(tablero, fila, col, num):
            tablero[fila][col] = num
            if resolver_aleatorio_backtracking_con_ramificacion(tablero):
                return True
            tablero[fila][col] = 0                         #Revisar
    return False

# Resolver Sudoku usando backtracking con poda de forma aleatoria
def resolver_aleatorio_backtracking_con_poda(tablero):
    global PASOS_ATRAS
    celda = encontrar_celda_mas_restringida(tablero)
    if not celda:
        return True
    fila, col = celda
    opciones = obtener_opciones_validas(tablero, fila, col)
    random.shuffle(opciones)  # Desordena las opciones para aleatoriedad
    
    for num in opciones:
        tablero[fila][col] = num
        if resolver_aleatorio_backtracking_con_poda(tablero):
            return True
        else:
            PASOS_ATRAS += 1
        tablero[fila][col] = 0
    return False

# Encontrar la celda con el menor número de opciones posibles
def encontrar_celda_mas_restringida(tablero):
    min_opciones = 10
    mejor_celda = None
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0:
                opciones = len(obtener_opciones_validas(tablero, fila, col))
                if opciones < min_opciones:
                    min_opciones = opciones
                    mejor_celda = (fila, col)
    return mejor_celda

# Obtener lista de números válidos para una celda específica
def obtener_opciones_validas(tablero, fila, col):
    opciones = set(range(1, 10)) # Inicia conjunto de opciones (todas las posibles, del 1 al 9)
    opciones -= set(tablero[fila]) # Quita de las opciones los números que ya están en la fila.
    opciones -= {tablero[i][col] for i in range(9)} # Quita los que ya están en la columna
    fila_inicio_cuadrante, col_inicio_cuadrante = (fila // 3) * 3, (col // 3) * 3 # Obtener coordenadas  del cuadrante
    opciones -= {tablero[i][j] for i in range(fila_inicio_cuadrante, fila_inicio_cuadrante + 3) for j in range(col_inicio_cuadrante, col_inicio_cuadrante + 3)} # Quita de las opciones los valores del cuadrante
    return list(opciones)

# Función para resolver el tablero usando el algoritmo elegido
def resolver_tablero_juego(tablero, algoritmo):
    global PASOS_ATRAS
    PASOS_ATRAS = 0
    if algoritmo == 1:
        return resolver_backtracking_puro(tablero)
    elif algoritmo == 2:
        return resolver_backtracking_con_ramificacion(tablero)
    elif algoritmo == 3:
        return resolver_backtracking_con_poda(tablero)
    else:
        print("Opción inválida.")
        return False
    
# Función para resolver el tablero usando el algoritmo elegido de forma aleatoria
def resolver_aleatorio_tablero_juego(tablero, algoritmo):
    if algoritmo == 1:
        return resolver_aleatorio_backtracking_puro(tablero)
    elif algoritmo == 2:
        return resolver_aleatorio_backtracking_con_ramificacion(tablero)
    elif algoritmo == 3:
        return resolver_aleatorio_backtracking_con_poda(tablero)
    else:
        print("Opción inválida.")
        return False

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

# Generar un tablero completo de Sudoku (con una única solución)
def generar_tablero_completo():
    """Genera un tablero completo y válido de Sudoku."""
    tablero = crear_tablero_sudoku_vacio()
    resolver_aleatorio_tablero_juego(tablero, 1)  # Utiliza backtracking puro
    return tablero


# Función para eliminar valores del tablero
def eliminar_valores(tablero, celdas_a_eliminar):
    """Elimina celdas del tablero."""
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

# ========================
# Funciones del Juego
# ========================

def seleccionar_modo():
    """Solicita al jugador que elija el modo de juego."""
    print("\nSeleccione el modo de juego:")
    print("1 - Generación y resolución automática por la PC")
    print("2 - Generación automática por la PC y resolución manual por el jugador")
    print("3 - Generación manual por el jugador y validación automática por la PC")
    while True:
        try:
            modo = int(input("Ingrese el número del modo deseado: "))
            if modo in [1, 2, 3]:
                return modo
            else:
                print("Modo inválido, intente nuevamente.")
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número.")

def seleccionar_algoritmo():
    """Solicita al jugador que seleccione un algoritmo de resolución."""
    print("\nSeleccione el algoritmo de resolución:")
    print("1 - Backtracking puro")
    print("2 - Backtracking con ramificación")
    print("3 - Backtracking con poda")
    while True:
        try:
            algoritmo = int(input("Ingrese el número del algoritmo deseado: "))
            if algoritmo in [1, 2, 3]:
                return algoritmo
            else:
                print("Opción inválida, intente nuevamente.")
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número.")

def seleccionar_dificultad():
    """Solicita al jugador que seleccione la dificultad del juego."""
    while True:
        try:
            dificultad = int(input("Seleccione dificultad (1: Fácil, 2: Normal, 3: Difícil, 4: Diabólico): "))
            if dificultad in [1, 2, 3, 4]:
                return [20, 40, 60, 75][dificultad - 1]
            else:
                print("Opción inválida, intente nuevamente.")
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número.")

# Modo de juego: PC crea y resuelve
def modo_pc_crea_y_resuelve(algoritmo):
    tablero_completo = generar_tablero_completo()
    celdas_a_eliminar = seleccionar_dificultad()

    # Eliminar algunas celdas para permitir jugar según la dificultad respetando la Unicidad resolutiva
    inicio = time.time()  # Tiempo de inicio
    tablero_jugable = eliminar_valores(tablero_completo, celdas_a_eliminar)
    fin = time.time()  # Tiempo de fin
    print(f"\nTiempo en el que se creó el tablero: {fin - inicio:.4f} segundos")

    imprimir_tablero(tablero_completo)

    # Medir el tiempo de resolución del tablero
    inicio = time.time()  # Tiempo de inicio
    resolver_tablero_juego(tablero_jugable, algoritmo)
    fin = time.time()  # Tiempo de fin

    # Imprimir el tiempo que tardó en resolver el tablero
    print(f"\nTiempo para resolver el tablero: {fin - inicio:.4f} segundos con {PASOS_ATRAS} retrocesos en su resolución")
    imprimir_tablero(tablero_jugable)


# Modo de juego: PC crea tablero, jugador resuelve
def modo_pc_crea_jugador_resuelve(algoritmo):
    tablero_completo = generar_tablero_completo()
    celdas_a_eliminar = seleccionar_dificultad()
    tablero_jugable = eliminar_valores(tablero_completo, celdas_a_eliminar)
    imprimir_tablero(tablero_jugable)
    print("\nEs tu turno de resolver el tablero. ¡Buena suerte!")

    # Bandera para controlar la primera iteración
    primera_iteracion = True

    # Bucle de entrada del usuario para llenar el tablero
    while True:
        # Solo pregunta si desea terminar después de la primera iteración
        if not primera_iteracion:
            terminar = input("¿Deseas seguir ingresando números o dejar que la computadora complete el tablero? (ingresa 's' para seguir, 'entregar' para terminar, 'pc' para que la PC lo complete): ").strip().lower()
            
            if terminar == 'entregar':
                if es_valido_sudoku(tablero_jugable):
                    print("\n¡Felicidades! El tablero está completo y tiene solución.")
                else:
                    print("\nEl tablero no tiene solución.")
                print("\nTablero finalizado por el jugador:")
                imprimir_tablero(tablero_jugable)
                break
            elif terminar == 'pc':
                print("\nLa computadora completará el tablero usando el algoritmo seleccionado...")
                resolver_tablero_juego(tablero_jugable, algoritmo)
                imprimir_tablero(tablero_jugable)
                break

        # Solicita la fila, columna y valor del usuario
        try:
            fila = int(input("Ingresa la fila (1-9): ")) - 1
            columna = int(input("Ingresa la columna (1-9): ")) - 1
            valor = int(input("Ingresa el valor (1-9): "))

            # Verifica que las coordenadas estén dentro de los límites
            if not (0 <= fila < 9 and 0 <= columna < 9 and 1 <= valor <= 9):
                print("Coordenadas o valor fuera de rango. Inténtalo de nuevo.")
                continue
            
            # Verifica si la celda ya tiene un valor
            if tablero_jugable[fila][columna] != 0:
                reemplazar = input("La celda ya tiene un valor. ¿Deseas reemplazarlo? (s/n): ").strip().lower()
                if reemplazar != 's':
                    print("Ingresa otro número.")
                    continue
            
            # Coloca el valor en el tablero
            tablero_jugable[fila][columna] = valor
            print("\nTablero actualizado:")
            imprimir_tablero(tablero_jugable)

            # Desactiva la bandera de la primera iteración después de la primera interacción
            primera_iteracion = False
        
        except ValueError:
            print("Entrada inválida. Asegúrate de ingresar números.")


# Modo de juego: Jugador crea tablero, PC lo valida
def modo_jugador_crea_pc_valida():
    tablero = crear_tablero_sudoku_vacio()
    print("Introduce el tablero de Sudoku a validar (use 0 para celdas vacías):")
    for i in range(9):
       fila = list(map(int, input(f"Fila {i+1} (9 números separados por espacio): ").split()))
       tablero[i] = fila
    print("\nValidando el tablero ingresado...")
    inicio = time.time()
    #if resolver_tablero_juego(tablero, algoritmo):
    if es_valido_sudoku(tablero):
        fin = time.time()
        print(f"El tablero ingresado es válido (tiempo de validación: {fin - inicio:.4f} segundos).")
        imprimir_tablero(tablero)
    else:
        fin = time.time()
        print(f"El tablero ingresado es inválido (tiempo de validación: {fin - inicio:.4f} segundos).")


# ========================
# Programa Principal
# ========================


# Inicialización de variables globales
PASOS_ATRAS = 0

# INICIO ----------------------------------------------->
print("\n<-- B I E N V E N I D O -->")
print("Haz empezado el juego del SUDOKU")
modo_juego = seleccionar_modo()
if modo_juego in [1,2]:
    algoritmo_resolucion = seleccionar_algoritmo()

# Ejecutar el modo de juego seleccionado
if modo_juego == 1:
    modo_pc_crea_y_resuelve(algoritmo_resolucion)
elif modo_juego == 2:
    modo_pc_crea_jugador_resuelve(algoritmo_resolucion)
elif modo_juego == 3:
    modo_jugador_crea_pc_valida()
else:
    print("Modo de juego no válido.")
