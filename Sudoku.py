import random
import time  # Importar el módulo para medir el tiempo
import sys
import copy
import heapq  # Para la cola de prioridad
import matplotlib.pyplot as plt

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
                        tablero[fila][col] = 0              
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
def generar_tablero_completo():
    """Genera un tablero completo y válido de Sudoku."""
    tablero = crear_tablero_sudoku_vacio()
    resolver_aleatorio_backtracking_puro(tablero)  # Utiliza backtracking puro
    return tablero


def contar_soluciones(tablero):
    """
    Cuenta cuántas soluciones tiene un tablero de Sudoku.
    Si hay más de 1 solución, se detiene temprano.
    """
    soluciones = [0]  # Usamos una lista mutable para mantener el conteo

    def resolver(tablero):
        if soluciones[0] > 1:
            #print("Se encontró mas de una solución")
            return  # Termina si encuentra más de 1 solución
        for fila in range(9):
            for col in range(9):
                if tablero[fila][col] == 0:
                    for num in range(1, 10):
                        if es_valido(tablero, fila, col, num):
                            tablero[fila][col] = num
                            resolver(tablero)
                            tablero[fila][col] = 0
                    return
        soluciones[0] += 1

    resolver(tablero)
    return soluciones[0]

# Función para eliminar valores del tablero
def eliminar_valores(tablero, celdas_a_eliminar):
    """
    Elimina celdas garantizando que el tablero tenga una única solución.
    """
    global CELDAS_JUGABLES
    CELDAS_JUGABLES = []
    celdas = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(celdas)

    for fila, col in celdas:
        if celdas_a_eliminar <= 0:
            break

        # Guardar el valor original de la celda
        valor_original = tablero[fila][col]
        tablero[fila][col] = 0

        # Verificar unicidad
        if contar_soluciones([fila[:] for fila in tablero]) == 1:
            CELDAS_JUGABLES.append((fila, col))  # Registrar la celda eliminada
            celdas_a_eliminar -= 1
        else:
            tablero[fila][col] = valor_original  # Restaurar el valor original si no es único

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
    global PASOS_ATRAS, NODOS_EXPLORADOS,SOLUCION# variable global
    for fila in range(9):
        for col in range(9):
            if tablero[fila][col] == 0:   # Si la celda está vacía
                for num in range(1, 10):  # Probar los números del 1 al 9                        
                    if es_valido(tablero, fila, col, num):  # Si el número es válido
                        tablero[fila][col] = num  # Colocamos el número
                        SOLUCION[(fila,col)] = num
                        NODOS_EXPLORADOS +=1
                        if resolver_backtracking_puro(tablero):  # Llamada recursiva
                            return True
                        else: # si uno de los nodos dio falso en su resolucion, volvemos atras
                            PASOS_ATRAS += 1
                        tablero[fila][col] = 0  #  volvemos atras Deshacer (retroceder)
                        del SOLUCION[(fila, col)]
                return False  # Si no encontramos una solución válida, retrocedemos
    return True  # Si hemos llenado todo el tablero correctamente


#FUNCIONES BRANCH & BOUND

# Resolver Sudoku usando Branch & Bound con cotas
def resolver_sudoku_bb_cotas(tablero):
    global PASOS_ATRAS, CELDAS_JUGABLES
    PASOS_ATRAS = 0
    CELDAS_JUGABLES = [(fila, col) for fila in range(9) for col in range(9) if tablero[fila][col] == 0]
    cota_superior = float('inf')
    cola_prioridad = crear_cola_prioridad(tablero)
    return bb_resolver_cotas(tablero, cola_prioridad, cota_superior)

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

        num_opciones = len(opciones)
        if num_opciones == 1:
            heapq.heappush(cola_prioridad, (num_opciones, -1000, fila, col, opciones))
            return cola_prioridad
        elif (len(opciones) <= 6):
            vecinos_afectados = contar_vecinos_restringidos_directo(tablero, fila, col)
            heapq.heappush(cola_prioridad, (len(opciones), -vecinos_afectados, fila, col, opciones)) 
        
    return cola_prioridad

def calcular_cota_superior(tablero):
    """
    Calcula una cota superior basada en:
    - El número de celdas vacías
    - La complejidad de completar esas celdas considerando restricciones
    """
    celdas_vacias = contar_celdas_vacias(tablero)
    if celdas_vacias == 0:
        return 0

    # Calculamos el factor de ramificación máximo
    max_opciones = 0
    total_restricciones = 0
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                opciones = len(obtener_opciones_validas(tablero, i, j))
                if opciones == 0:
                    return float('inf')  # No hay solución posible
                max_opciones = max(max_opciones, opciones)
                total_restricciones += contar_vecinos_restringidos_directo(tablero, i, j)

    # La cota superior considera tanto las opciones como las restricciones
    return celdas_vacias * max_opciones + total_restricciones

# Resolver utilizando Branch & Bound con cotas
def bb_resolver_cotas(tablero, cola_prioridad, mejor_cota):
    global PASOS_ATRAS, NODOS_EXPLORADOS,SOLUCION

    # Contar celdas vacías
    celdas_vacias = contar_celdas_vacias(tablero)

    # Si no hay celdas vacías, el tablero está completo
    if celdas_vacias == 0:
        return True  # No necesitamos recalcular la cota

    # Si la cola está vacía pero aún hay celdas vacías, el tablero no tiene solución
    if not cola_prioridad:
        return False

    # Calculamos la cota superior para este estado
    cota_actual = calcular_cota_superior(tablero)

    # Si la cota actual es peor que la mejor conocida, podamos esta rama
    if cota_actual >= mejor_cota:
        return False
    
    # Extraer la celda más prometedora
    _, _, fila, col, opciones = heapq.heappop(cola_prioridad)

    for num in opciones:
        # Asignar el número a la celda
        tablero[fila][col] = num
        SOLUCION[(fila,col)] = num
        NODOS_EXPLORADOS += 1 

        # Actualizar la cola de prioridad
        nueva_cola = crear_cola_prioridad(tablero)

        if bb_resolver_cotas(tablero, nueva_cola, cota_actual):
            return True

        # Si no es solución, retroceder
        tablero[fila][col] = 0
        del SOLUCION[(fila, col)]
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
    print("4 - Ejecutar los tests")
    while True:
        try:
            modo = int(input("Ingrese el número del modo deseado: "))
            if modo in [1, 2, 3, 4]:
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
            dificultad = int(input("Seleccione dificultad (1: Fácil, 2: Normal, 3: Difícil): "))
            if dificultad in [1, 2, 3]:
                return [random.randint(31, 41), random.randint(41, 51), random.randint(51, 63)][dificultad - 1]
            else:
                print("Opción inválida, intente nuevamente.")
        except ValueError:
            print("Entrada no válida. Por favor, ingrese un número.")

# Modo de juego: PC crea y resuelve
def modo_pc_crea_y_resuelve(algoritmo):
    inicio = time.time()  # Tiempo de inicio
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
    print(f"\nSe han explorado {NODOS_EXPLORADOS} NODOS para llegar a la solucion")
    camino = " ---> ".join([f"({fila}, {col}): {valor}" for (fila, col), valor in SOLUCION.items()])
    print("Camino de solución:\n" + camino)
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
# Pruebas
# ========================

def generar_pruebas_rendimiento():
    """
    Genera una serie de pruebas para comparar los algoritmos y analizar unicidad de soluciones.
    """
    num_pruebas = 10  # Número de tableros a probar para cada configuración
    tiempos_backtracking = []
    tiempos_bb = []
    resultados_unicidad = {i: 0 for i in range(17, 82)}  # 17 es el mínimo teórico para unicidad
    
    print("\nIniciando pruebas de rendimiento...")
    
    # Pruebas de velocidad
    for i in range(num_pruebas):
        print(f"-----PRUEBA NUMERO {i+1}------")
        tablero_original = generar_tablero_completo()
        # Prueba con diferentes números de celdas eliminadas
        for celdas_eliminadas in [20, 30, 40, 50, 60]:
            tablero_prueba = copy.deepcopy(tablero_original)
            tablero_test = eliminar_valores(tablero_prueba, celdas_eliminadas)
            
            # Medir tiempo backtracking
            global NODOS_EXPLORADOS
            tablero_bt = copy.deepcopy(tablero_test)
            inicio_bt = time.time()
            resolver_backtracking_puro(tablero_bt)
            tiempo_bt = time.time()
            tiempos_backtracking.append((celdas_eliminadas, (tiempo_bt-inicio_bt), NODOS_EXPLORADOS))

            # Medir tiempo Branch & Bound
            NODOS_EXPLORADOS = 0
            tablero_bb = copy.deepcopy(tablero_test)
            inicio_bb = time.time()
            resolver_sudoku_bb_cotas(tablero_bb)
            tiempo_bb = time.time()
            tiempos_bb.append((celdas_eliminadas, (tiempo_bb - inicio_bb), NODOS_EXPLORADOS))
            
            print(f"\nPrueba con {celdas_eliminadas} celdas eliminadas:")
            print(f"Backtracking: {(tiempo_bt-inicio_bt):.4f} segundos, Nodos explorados: {tiempos_backtracking[-1][2]}")
            print(f"Branch & Bound: {(tiempo_bb - inicio_bb):.4f} segundos, Nodos explorados: {tiempos_bb[-1][2]}")
            print(tablero_prueba)

    # Prueba de unicidad de solución
    print("\nAnalizando unicidad de soluciones...")
    for pistas in range(81, 16, -1):  # De más pistas a menos
        soluciones_unicas = 0
        for _ in range(5):  # 5 tableros por cada cantidad de pistas
            tablero_original = generar_tablero_completo()
            tablero_prueba = copy.deepcopy(tablero_original)
            celdas_a_eliminar = 81 - pistas
            tablero_test = eliminar_valores(tablero_prueba, celdas_a_eliminar)
            
            if tiene_solucion_unica(tablero_test):
                soluciones_unicas += 1
        
        resultados_unicidad[pistas] = soluciones_unicas / 5  # Proporción de soluciones únicas
        print(f"Pistas: {pistas}, Proporción de soluciones únicas: {resultados_unicidad[pistas]:.2f}")
        
        # Si encontramos el punto donde todas las soluciones son únicas, podemos parar
        if resultados_unicidad[pistas] == 1.0 and resultados_unicidad.get(pistas - 1, 0) < 1.0:
            print(f"\nUmbral de unicidad encontrado en aproximadamente {pistas} pistas")
            break

    return tiempos_backtracking, tiempos_bb, resultados_unicidad

def tiene_solucion_unica(tablero):
    """
    Verifica si un tablero tiene solución única contando el número de soluciones posibles.
    Retorna True si solo hay una solución, False en caso contrario.
    """
    soluciones = [0]  # Usamos una lista para poder modificarla en la función recursiva
    
    def contar_soluciones(tablero):
        if soluciones[0] > 1:  # Si ya encontramos más de una solución, no seguimos buscando
            return
            
        if es_valido_sudoku(tablero, True):
            soluciones[0] += 1
            return
            
        for i in range(9):
            for j in range(9):
                if tablero[i][j] == 0:
                    for num in range(1, 10):
                        if es_valido(tablero, i, j, num):
                            tablero[i][j] = num
                            contar_soluciones(tablero)
                            tablero[i][j] = 0
                    return
    
    tablero_copia = copy.deepcopy(tablero)
    contar_soluciones(tablero_copia)
    return soluciones[0] == 1

def analizar_resultados(tiempos_bt, tiempos_bb, resultados_unicidad):
    """
    Analiza y muestra los resultados de las pruebas, y genera gráficos.
    """
    print("\nResultados del análisis:")
    
    # Análisis de tiempos y nodos
    tiempos_por_celdas_bt = {}
    tiempos_por_celdas_bb = {}
    nodos_por_celdas_bt = {}
    nodos_por_celdas_bb = {}

    for celdas, tiempo, nodos in tiempos_bt:
        if celdas not in tiempos_por_celdas_bt:
            tiempos_por_celdas_bt[celdas] = []
            nodos_por_celdas_bt[celdas] = []
        tiempos_por_celdas_bt[celdas].append(tiempo)
        nodos_por_celdas_bt[celdas].append(nodos)

    for celdas, tiempo, nodos in tiempos_bb:
        if celdas not in tiempos_por_celdas_bb:
            tiempos_por_celdas_bb[celdas] = []
            nodos_por_celdas_bb[celdas] = []
        tiempos_por_celdas_bb[celdas].append(tiempo)
        nodos_por_celdas_bb[celdas].append(nodos)

    # Preparar datos para gráficos
    celdas_eliminadas = sorted(tiempos_por_celdas_bt.keys())
    tiempos_promedio_bt = [sum(tiempos_por_celdas_bt[c]) / len(tiempos_por_celdas_bt[c]) for c in celdas_eliminadas]
    tiempos_promedio_bb = [sum(tiempos_por_celdas_bb[c]) / len(tiempos_por_celdas_bb[c]) for c in celdas_eliminadas]
    nodos_promedio_bt = [sum(nodos_por_celdas_bt[c]) / len(nodos_por_celdas_bt[c]) for c in celdas_eliminadas]
    nodos_promedio_bb = [sum(nodos_por_celdas_bb[c]) / len(nodos_por_celdas_bb[c]) for c in celdas_eliminadas]

    print("\nTiempos promedio por número de celdas eliminadas:")
    for celdas, tiempo_bt, tiempo_bb, nodos_bt, nodos_bb in zip(celdas_eliminadas, tiempos_promedio_bt, tiempos_promedio_bb, nodos_promedio_bt, nodos_promedio_bb):
        print(f"\nCeldas eliminadas: {celdas}")
        print(f"Backtracking: {tiempo_bt:.4f} segundos")
        print(f"Branch & Bound: {tiempo_bb:.4f} segundos")
        print(f"Nodos explorados BT: {nodos_bt:.0f}")
        print(f"Nodos explorados BB: {nodos_bb:.0f}")
        print(f"Diferencia (BB - BT): {tiempo_bb - tiempo_bt:.4f} segundos")
        print(f"Mejora porcentual: {((tiempo_bt - tiempo_bb) / tiempo_bt * 100):.2f}%")

    # Crear gráfico de barras para tiempos de ejecución
    plt.figure(figsize=(12, 6))
    plt.bar([c - 0.2 for c in celdas_eliminadas], tiempos_promedio_bt, width=0.4, label='Backtracking', alpha=0.6)
    plt.bar([c + 0.2 for c in celdas_eliminadas], tiempos_promedio_bb, width=0.4, label='Branch & Bound', alpha=0.6)
    plt.xlabel('Celdas Eliminadas')
    plt.ylabel('Tiempo Promedio (segundos)')
    plt.title('Comparación de Tiempos de Ejecución')
    plt.xticks(celdas_eliminadas)
    plt.legend()
    plt.show()

    # Crear gráfico de barras para nodos explorados
    plt.figure(figsize=(12, 6))
    plt.bar([c - 0.2 for c in celdas_eliminadas], nodos_promedio_bt, width=0.4, label='Nodos BT', alpha=0.6)
    plt.bar([c + 0.2 for c in celdas_eliminadas], nodos_promedio_bb, width=0.4, label='Nodos BB', alpha=0.6)
    plt.xlabel('Celdas Eliminadas')
    plt.ylabel('Nodos Explorados (promedio)')
    plt.title('Comparación de Nodos Explorados')
    plt.xticks(celdas_eliminadas)
    plt.legend()
    plt.show()

    # Crear gráfico de líneas para unicidad de soluciones
    plt.figure(figsize=(12, 6))
    pistas = sorted(resultados_unicidad.keys())
    unicidad = [resultados_unicidad[p] for p in pistas]
    plt.plot(pistas, unicidad, marker='o', linestyle='-', color='b')
    plt.xlabel('Número de Pistas')
    plt.ylabel('Proporción de Soluciones Únicas')
    plt.title('Unicidad de Soluciones por Número de Pistas')
    plt.grid(True)
    plt.show()

# Modificar la función de ejecución de pruebas para incluir gráficos
def ejecutar_pruebas_completas():
    print("Iniciando pruebas completas...")
    tiempos_bt, tiempos_bb, resultados_unicidad = generar_pruebas_rendimiento()
    analizar_resultados(tiempos_bt, tiempos_bb, resultados_unicidad)

# ========================
# Programa Principal
# ========================

# Inicialización de variables globales
PASOS_ATRAS = 0
NODOS_EXPLORADOS= 0
DISTINTAS_SOLUCIONES=0
CELDAS_JUGABLES=[]
SOLUCION = {}


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
elif modo_juego == 4:
    ejecutar_pruebas_completas()
else:
    print("Modo de juego no válido.")