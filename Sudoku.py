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
import copy

import heapq  # Para la cola de prioridad

# ========================
# Funciones de utilidades
# ========================
def barra_de_carga(iterable, total, prefix='', length=40, fill='█'):
    """Muestra una barra de carga en la terminal en la misma línea."""
    percent = (len(iterable) / total)
    filled_length = int(length * percent)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent * 100:.1f}% Completado')
    sys.stdout.flush()
    
# ========================
# Creacion y armado del tablero
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
            # Verifica si la celda actual está en CELDAS_JUGABLES
            if (i, j) in CELDAS_JUGABLES:
                # Código ANSI para texto amarillo
                print(f"\033[93m{tablero[i][j] if tablero[i][j] != 0 else '.'}\033[0m", end=" ")
            else:
                print(tablero[i][j] if tablero[i][j] != 0 else ".", end=" ")
        print()

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


# Función para resolver el tablero usando el algoritmo elegido
def resolver_tablero_juego(tablero, algoritmo):
    global PASOS_ATRAS
    PASOS_ATRAS = 0
    if algoritmo == 1:
        return resolver_backtracking_puro(tablero)
    elif algoritmo == 2:
        return resolver_sudoku_bb_cotas(tablero)
    else:
        print("Opción inválida.")
        return False

# Generar un tablero completo de Sudoku (con una única solución)
def generar_tablero_completo(algoritmo):
    """Genera un tablero completo y válido de Sudoku."""
    tablero = crear_tablero_sudoku_vacio()
    resolver_aleatorio_backtracking_puro(tablero)  # Utiliza backtracking puro
    return tablero


# Función para eliminar valores del tablero
def eliminar_valores(tablero, celdas_a_eliminar):
    global CELDAS_JUGABLES
    """Elimina celdas del tablero."""
    celdas = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(celdas)

    #For para barra de carga (No es necesario)
    for i in range(celdas_a_eliminar):          
        # Mostrar barra de carga después de cada eliminación
        barra_de_carga(range(i + 1), celdas_a_eliminar, prefix='Creando Tablero de Juego')

        fila, col = celdas[i]
        tablero[fila][col] = 0
        CELDAS_JUGABLES.append((fila,col))

    sys.stdout.write('\n')  # Para mover el cursor a la siguiente línea después de la barra

    return tablero

# ========================
# Validacion
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

def es_valido_sudoku(tablero, validarCeros = True):
    # Verificar que cada fila contiene números del 1 al 9 sin repeticiones
    for fila in tablero:
        if validarCeros and 0 in fila:
            return False
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

def es_modificable(posicion, CELDAS_JUGABLES):
    """Verifica si una posición está entre las celdas eliminadas y es modificable."""
    return posicion in CELDAS_JUGABLES

# ========================
#  Resolución
# ========================
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


# #FUNCIONES BRANCH&BOUND

# Resolver Sudoku usando Branch & Bound con cotas
def resolver_sudoku_bb_cotas(tablero):
    global PASOS_ATRAS, CELDAS_VACIAS_MIN, CELDAS_JUGABLES
    PASOS_ATRAS = 0
    #CELDAS_VACIAS_MIN = contar_celdas_vacias(tablero)  # Inicializamos la cota superior
    CELDAS_JUGABLES = [(fila, col) for fila in range(9) for col in range(9) if tablero[fila][col] == 0]
    cola_prioridad = crear_cola_prioridad(tablero)
    return bb_resolver_cotas(tablero, cola_prioridad, float('inf'))

# Crear una cola de prioridad con las celdas más restringidas
def crear_cola_prioridad(tablero):
    cola_prioridad = []
    celdas_vacias = [(fila, col) for fila in range(9) for col in range(9) if tablero[fila][col] == 0]

    for fila, col in celdas_vacias:
        if tablero[fila][col] != 0:
            continue 

        opciones = obtener_opciones_validas(tablero, fila, col)

        if not opciones:  # Si no hay opciones válidas, podar esta rama
            return []  # Detenemos y señalamos que no hay solución posible

        if(len(opciones) == 1):
            heapq.heappush(cola_prioridad, (len(opciones), -1, fila, col, opciones)) 
            return cola_prioridad
        elif(len(opciones) <= 6):
            vecinos_afectados = contar_vecinos_restringidos_directo(tablero, fila, col)
            heapq.heappush(cola_prioridad, (len(opciones), -vecinos_afectados, fila, col, opciones)) 

        # opciones_validas = list(opciones)

        # Simular asignaciones y validar
        # for num in opciones_validas:
        #     tablero[fila][col] = num  # Simulación

        #     if not cota_valida(tablero):  # Verificar si deja otras celdas sin opciones
        #         tablero[fila][col] = 0  # Deshacer
        #         opciones.remove(num)    # Si esta opcion me lleva a una rama inválida, la elimino
        #         continue  # No insertar esta opción
        #     tablero[fila][col] = 0  # Deshacer

        # if not opciones: 
        #     return []
        
    return cola_prioridad

# Resolver utilizando Branch & Bound con cotas
def bb_resolver_cotas(tablero, cola_prioridad, cota_sup):
    global PASOS_ATRAS, CELDAS_VACIAS_MIN

    if not cola_prioridad:  # Si la cola está vacía, el tablero está completo
        return True

    # Contar celdas vacías
    celdas_vacias = contar_celdas_vacias(tablero)

    # Si no hay celdas vacías, el tablero está resuelto
    if celdas_vacias == 0:
        return True


    # Podar si no mejora la cota superior
    # if celdas_vacias >= cota_sup:  # Si no reduce el número de celdas vacías
    #     print("Se ha podado una rama")
    #     return False

    # Actualizar cota superior
    # cota_sup_nueva= celdas_vacias
    if celdas_vacias < cota_sup:
        cota_sup_nueva = celdas_vacias

    # Extraer la celda más restringida
    _, _, fila, col, opciones = heapq.heappop(cola_prioridad) 
    for num in opciones:
        # Asignar el número a la celda
        tablero[fila][col] = num

        # Actualizar la cola de prioridad
        nueva_cola = crear_cola_prioridad(tablero)

        # Verificar cotas
        if cota_valida(tablero):  # Cota inferior
            if bb_resolver_cotas(tablero, nueva_cola,cota_sup_nueva):  # Continuar exploración
                return True

        # bb_resolver_cotas(tablero, nueva_cola, cota_sup_nueva)

        # Si no es solución, retroceder
        tablero[fila][col] = 0
        PASOS_ATRAS += 1

    return False

def contar_vecinos_restringidos_directo(tablero, fila, col):
    vecinos_restringidos = 0
    # Contar vecinos en fila y columna
    vecinos_restringidos += sum(1 for i in range(9) if tablero[fila][i] == 0 and i != col)
    vecinos_restringidos += sum(1 for i in range(9) if tablero[i][col] == 0 and i != fila)
    # Contar vecinos en el bloque 3x3
    fila_inicio, col_inicio = (fila // 3) * 3, (col // 3) * 3
    vecinos_restringidos += sum(
        1 for i in range(fila_inicio, fila_inicio + 3) for j in range(col_inicio, col_inicio + 3)
        if tablero[i][j] == 0 and i != fila and j != col
    )
    return vecinos_restringidos

# Verificar si la cota inferior es válida
def cota_valida(tablero):
    for fila, col in CELDAS_JUGABLES:
        if tablero[fila][col] == 0 and not obtener_opciones_validas(tablero, fila, col):
            return False
    return True

# Contar celdas vacías en el tablero
def contar_celdas_vacias(tablero):
    return sum(1 for fila in tablero for celda in fila if celda == 0)

# Obtener lista de números válidos para una celda específica
def obtener_opciones_validas(tablero, fila, col):
    opciones = set(range(1, 10))
    opciones -= set(tablero[fila])
    opciones -= {tablero[i][col] for i in range(9)}
    fila_inicio, col_inicio = (fila // 3) * 3, (col // 3) * 3
    opciones -= {tablero[i][j] for i in range(fila_inicio, fila_inicio + 3) for j in range(col_inicio, col_inicio + 3)}
    return list(opciones)

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
    print("2 - Branch & Bound")
    while True:
        try:
            algoritmo = int(input("Ingrese el número del algoritmo deseado: "))
            if algoritmo in [1, 2]:
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
    inicio = time.time()  # Tiempo de inicio
    tablero_completo = generar_tablero_completo(algoritmo)
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
    tablero_jugable_PC = copy.deepcopy(tablero_jugable)
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
                    print("\nEl tablero esta incompleto o es inválido :( .")
                print("\nTablero finalizado por el jugador:")
                imprimir_tablero(tablero_jugable)
                break
            elif terminar == 'pc':
                print("\nLa computadora resolverá el tablero usando el algoritmo seleccionado...")
                resolver_tablero_juego(tablero_jugable_PC, algoritmo)
                imprimir_tablero(tablero_jugable_PC)
                break

        # Solicita la fila, columna y valor del usuario
        try:
            fila = int(input("Ingresa la fila (1-9): ")) - 1
            columna = int(input("Ingresa la columna (1-9): ")) - 1
            valor = int(input("Ingresa el valor (1-9): "))
            if not es_modificable((fila,columna), CELDAS_JUGABLES):
                print("No podes alterar una celda Original!! Proba con otra")
                continue
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
       ceros =  len([numero for numero in fila if numero != 0])
    print("\nValidando el tablero ingresado...")
    inicio = time.time()
    #if resolver_tablero_juego(tablero, algoritmo):
    if es_valido_sudoku(tablero, False):
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
CELDAS_JUGABLES=[]
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